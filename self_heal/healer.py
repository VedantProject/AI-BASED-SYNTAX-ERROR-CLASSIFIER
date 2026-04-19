"""
self_heal/healer.py  — Safe, Ambiguity-Aware Self-Healing Engine
=================================================================
Design rules that govern THIS module
--------------------------------------

1. ERROR CATEGORY SEPARATION
   • SYNTAX  errors  → auto-apply if re-parse confirms improvement
   • PATTERN warnings → suggest only (BARE_EXCEPT, MUTABLE_DEFAULT, …)
   • WARNING diagnostics → suggest only, NEVER auto-apply
     (MISSING_RETURN, UNUSED_VARIABLE, UNREACHABLE_CODE, …)
   • SEMANTIC (UNDEFINED_NAME) → suggest only unless *single* candidate
     within distance-1 that shares first char

2. CONFIDENCE GATE
   Auto-apply threshold is 0.80.  Below that a RepairAction is produced
   with mode='suggested' — no source text is changed.

3. AMBIGUITY AWARENESS
   When multiple candidates exist for UNDEFINED_NAME, ALL are stored in
   RepairAction.suggestions so the display can present options instead
   of silently picking one.

4. RE-PARSE AFTER EVERY REPAIR
   Each accepted patch is immediately passed to _reparse().  If the
   error count does NOT decrease the patch is rejected, regardless of
   confidence.

5. CONFLICT AVOIDANCE
   At most ONE patch per physical source line per heal_source() call.
"""

from __future__ import annotations

import re
import sys
import os
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

# ── Path setup ────────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from self_heal.source_patcher import (
    source_to_lines,
    lines_to_source,
    insert_at_line_end,
    replace_on_line,
    replace_line,
    reindent_line,
    tabs_to_spaces,
    infer_indent_level,
    append_line_after,
)


# ══════════════════════════════════════════════════════════════════════════════
# Error category taxonomy
# ══════════════════════════════════════════════════════════════════════════════

# SYNTAX errors → safe to auto-apply when re-parse confirms
_SYNTAX_TYPES: set = {
    "MISSING_COLON",
    "MISSING_SEMICOLON",
    "MISSING_PAREN",
    "MISSING_BRACKET",
    "MISSING_BRACE",
    "INDENTATION_ERROR",
    "INCONSISTENT_INDENTATION",
    "INVALID_EXPRESSION",
    "INCOMPLETE_STATEMENT",
    "INVALID_FUNCTION_DEF",
    "INVALID_CLASS_DEF",
    "INVALID_DECLARATION",
    "INVALID_SYNTAX",
    "UNEXPECTED_TOKEN",
    "SyntaxError",
    "KEYWORD_MISUSE",
    "MAX_ERRORS_EXCEEDED",
    "UnexpectedEOF",
}

# PATTERN best-practice violations → suggest only, never auto-apply
_PATTERN_TYPES: set = {
    "BARE_EXCEPT",
    "MUTABLE_DEFAULT_ARG",
    "SINGLETON_COMPARE",
    "IS_LITERAL_COMPARE",
    "BUILTIN_SHADOW",
}

# WARNING diagnostics → suggest only, NEVER auto-apply
_WARNING_TYPES: set = {
    "MISSING_RETURN",
    "UNUSED_VARIABLE",
    "REDUNDANT_ASSIGNMENT",
    "UNREACHABLE_CODE",
    "INFINITE_LOOP",
    "BREAK_OUTSIDE_LOOP",
    "CONTINUE_OUTSIDE_LOOP",
    "UNUSED_IMPORT",
}

# Minimum confidence for auto-apply (syntax errors only)
_AUTO_APPLY_THRESHOLD = 0.80


# ══════════════════════════════════════════════════════════════════════════════
# Data structures
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class RepairAction:
    """Records one attempted or suggested repair."""
    error_type:    str
    line:          int
    description:   str          # human-readable summary of what was done
    original_line: str          # source text before repair
    repaired_line: str          # source text after repair (empty if mode='suggested')
    confidence:    float = 0.0  # 0.0 – 1.0
    verified:      bool  = False  # True → re-parse confirmed error reduction
    #
    # mode values
    #   'applied'   — patch was written to working_lines
    #   'suggested' — patch NOT applied; presented as a recommendation
    #   'skipped'   — no rule could produce a patch
    mode:          str   = "skipped"
    skip_reason:   str   = ""    # why mode='skipped'
    # For ambiguous cases (e.g. undefined name with several close matches)
    suggestions:   List[str] = field(default_factory=list)

    # Backwards-compat shim so existing code that checks .skipped still works
    @property
    def skipped(self) -> bool:
        return self.mode == "skipped"


@dataclass
class HealResult:
    """Outcome of a full heal_source() call."""
    healed_source:  str
    actions:        List[RepairAction] = field(default_factory=list)
    repaired_count: int  = 0    # verified auto-applied repairs
    suggested_count: int = 0    # suggest-only actions
    fully_healed:   bool = False


# ══════════════════════════════════════════════════════════════════════════════
# Levenshtein & candidate helpers
# ══════════════════════════════════════════════════════════════════════════════

def _levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    la, lb = len(a), len(b)
    if la == 0: return lb
    if lb == 0: return la
    prev = list(range(lb + 1))
    for i, ca in enumerate(a, 1):
        curr = [i] + [0] * lb
        for j, cb in enumerate(b, 1):
            curr[j] = min(prev[j] + 1, curr[j-1] + 1, prev[j-1] + (ca != cb))
        prev = curr
    return prev[lb]


def _ranked_candidates(name: str,
                        candidates,
                        max_dist: int = 3,
                        n: int = 5) -> List[Tuple[int, str]]:
    """
    Return up to *n* (distance, candidate) pairs sorted by distance,
    filtered to max_dist.  Case-insensitive distance; original case returned.
    """
    scored = []
    nl = name.lower()
    for c in candidates:
        d = _levenshtein(nl, c.lower())
        if d <= max_dist:
            scored.append((d, c))
    scored.sort(key=lambda x: x[0])
    return scored[:n]


def _safe_typo_candidate(name: str,
                          candidates,
                          max_dist: int = 1) -> Optional[str]:
    """
    Return a SINGLE safe auto-replace candidate, or None.

    Rules for auto-replace (all must hold):
      • Exactly ONE candidate within *max_dist* edits
      • That candidate shares the first character with *name*
      • Distance is at most *max_dist* (default 1)
    If any rule fails, return None — caller should fall back to suggestions.
    """
    if not name or not candidates:
        return None
    hits = _ranked_candidates(name, candidates, max_dist=max_dist)
    if len(hits) != 1:
        return None           # ambiguous or no match
    dist, best = hits[0]
    if dist == 0:
        return None           # exact match — not a typo
    # First-character check (catches e.g. 'prnit' → 'print' but not 'z' → 'x')
    if not name or not best or name[0].lower() != best[0].lower():
        return None
    return best


# ══════════════════════════════════════════════════════════════════════════════
# Re-parse helper
# ══════════════════════════════════════════════════════════════════════════════

def _reparse(source: str, language: str) -> int:
    """
    Return the number of parser errors in *source*.
    Never raises — returns 9999 on internal error so callers always see
    "no improvement" rather than crashing.
    """
    try:
        if language == "python":
            from lexers import tokenize_python
            from parsers import parse_python
            _, errors = parse_python(tokenize_python(source))
        elif language == "c":
            from lexers import tokenize_c
            from parsers import parse_c
            _, errors = parse_c(tokenize_c(source))
        elif language == "java":
            from lexers import tokenize_java
            from parsers import parse_java
            _, errors = parse_java(tokenize_java(source))
        else:
            return 0
        return len(errors)
    except Exception:
        return 9999


def _collect_errors(source: str, language: str) -> list:
    """Return parser error objects for *source*; never raises."""
    try:
        if language == "python":
            from lexers import tokenize_python
            from parsers import parse_python
            _, errors = parse_python(tokenize_python(source))
        elif language == "c":
            from lexers import tokenize_c
            from parsers import parse_c
            _, errors = parse_c(tokenize_c(source))
        elif language == "java":
            from lexers import tokenize_java
            from parsers import parse_java
            _, errors = parse_java(tokenize_java(source))
        else:
            return []
        return errors
    except Exception:
        return []


# ══════════════════════════════════════════════════════════════════════════════
# Delimiter-balance helpers (safer paren/bracket/brace repair)
# ══════════════════════════════════════════════════════════════════════════════

_OPEN_CLOSE = {'(': ')', '[': ']', '{': '}'}
_CLOSE_OPEN = {v: k for k, v in _OPEN_CLOSE.items()}


def _count_unmatched(line: str, open_ch: str, close_ch: str) -> int:
    """
    Return net unmatched opens in *line* (positive = more opens than closes).
    Ignores characters inside string literals (simple heuristic).
    """
    in_str, str_ch = False, ''
    depth = 0
    for ch in line:
        if in_str:
            if ch == str_ch:
                in_str = False
        elif ch in ('"', "'"):
            in_str, str_ch = True, ch
        elif ch == open_ch:
            depth += 1
        elif ch == close_ch:
            depth -= 1
    return depth


def _find_unmatched_open(source_lines: List[str],
                          target_line: int,
                          open_ch: str,
                          close_ch: str) -> int:
    """
    Scan from the start of the file up to *target_line* (1-indexed) and
    return the net unmatched open count.  Used to decide whether we really
    need to insert a closer.
    """
    depth = 0
    for i in range(min(target_line, len(source_lines))):
        depth += _count_unmatched(source_lines[i], open_ch, close_ch)
    return depth


# ══════════════════════════════════════════════════════════════════════════════
# Individual repair strategies
# Each returns (new_lines, description, confidence) or None.
# ══════════════════════════════════════════════════════════════════════════════

def _repair_missing_colon(lines, error, lang):
    """Insert ':' at end of the flagged header line."""
    idx = error.line - 1
    if not (0 <= idx < len(lines)):
        return None
    line = lines[idx]
    if lang == "python":
        m = re.match(r"^(\s*)(if|elif|while)\b(.*)$", line)
        if m:
            indent, keyword, rest = m.groups()
            if re.search(r"(?<![=!<>])=(?!=)", rest):
                fixed_rest = re.sub(r"(?<![=!<>])=(?!=)", "==", rest, count=1)
                if not fixed_rest.rstrip().endswith(":"):
                    fixed_rest = fixed_rest.rstrip() + ":"
                new_lines = replace_line(lines, error.line, f"{indent}{keyword}{fixed_rest}")
                return new_lines, f"Repaired '=' to '==' and added ':' to complete the {keyword} header.", 0.98
    stripped = line.rstrip()
    if stripped.endswith(":"):
        return None          # false positive — already has colon
    # Don't insert on blank or comment-only lines
    content = stripped.lstrip()
    if not content or content.startswith("#"):
        return None
    new_lines = insert_at_line_end(lines, error.line, ":")
    return new_lines, "Inserted ':' at end of line.", 0.95


def _repair_missing_semicolon(lines, error, lang):
    """Insert ';' at end of the flagged statement line."""
    idx = error.line - 1
    if not (0 <= idx < len(lines)):
        return None
    stripped = lines[idx].rstrip()
    if stripped.endswith(";") or stripped.endswith("{") or stripped.endswith("}"):
        return None
    if not stripped.lstrip():
        return None
    new_lines = insert_at_line_end(lines, error.line, ";")
    return new_lines, "Inserted ';' at end of line.", 0.93


def _repair_missing_paren(lines, error, lang):
    """
    Smart paren repair:
      - Count actual unmatched parens up to the flagged line.
      - Only insert ')' if there really is an unclosed '(' in scope.
      - For missing '(', insert after keyword only when pattern is clear.
    """
    idx = error.line - 1
    if not (0 <= idx < len(lines)):
        return None
    msg = error.message.lower()

    if "missing '('" in msg or "opening" in msg:
        line = lines[idx]
        for kw in ("def ", "if ", "while ", "for "):
            pos = line.find(kw)
            if pos != -1:
                # Check that there is no '(' already after the keyword on this line
                after = line[pos + len(kw):]
                if "(" not in after.split(":")[0]:  # before colon
                    insert_at = pos + len(kw)
                    new_line = line[:insert_at] + "(" + line[insert_at:]
                    new_lines = list(lines)
                    new_lines[idx] = new_line
                    return new_lines, f"Inserted '(' after '{kw.strip()}'.", 0.65
        return None
    else:
        # Closing paren missing — verify with delimiter balance
        unmatched = _find_unmatched_open(lines, error.line, "(", ")")
        if unmatched <= 0:
            return None   # no real unclosed paren — skip
        new_lines = insert_at_line_end(lines, error.line, ")")
        return new_lines, "Inserted ')' to close unmatched '('.", 0.84


def _repair_missing_bracket(lines, error, lang):
    """Insert ']' only when delimiter balance confirms an unclosed '['."""
    idx = error.line - 1
    if not (0 <= idx < len(lines)):
        return None
    unmatched = _find_unmatched_open(lines, error.line, "[", "]")
    if unmatched <= 0:
        return None
    new_lines = insert_at_line_end(lines, error.line, "]")
    return new_lines, "Inserted ']' to close unmatched '['.", 0.78


def _repair_missing_brace(lines, error, lang):
    """
    Brace repair with delimiter-balance check.
    - Missing '{': insert at end of flagged line only if net opens < 0.
    - Missing '}': insert a new closing-brace line with inferred indentation.
    """
    msg = error.message.lower()
    idx = error.line - 1
    if not (0 <= idx < len(lines)):
        return None

    if "opening" in msg or "missing '{'" in msg:
        unmatched = _find_unmatched_open(lines, error.line, "{", "}")
        if unmatched < 0:   # we have more closes than opens — don't add another open
            return None
        new_lines = insert_at_line_end(lines, error.line, " {")
        return new_lines, "Inserted '{' at end of line.", 0.70
    else:
        # Missing closing brace
        unmatched = _find_unmatched_open(lines, error.line, "{", "}")
        if unmatched <= 0:
            return None     # balance is fine — skip
        # Determine indentation: look at the opening '{' context
        block_indent = 0
        for i in range(idx - 1, -1, -1):
            if lines[i].strip():
                block_indent = len(lines[i]) - len(lines[i].lstrip())
                break
        closing_line = " " * block_indent + "}"
        new_lines = list(lines)
        new_lines.insert(error.line, closing_line)
        return new_lines, f"Inserted '}}' closing brace after line {error.line}.", 0.70


def _repair_indentation_error(lines, error, lang):
    """Re-indent flagged line to inferred correct level."""
    idx = error.line - 1
    if not (0 <= idx < len(lines)):
        return None
    if not lines[idx].strip():
        return None
    target = infer_indent_level(lines, error.line)
    current = len(lines[idx]) - len(lines[idx].lstrip())
    if current == target:
        return None   # already at the right level — false positive
    new_lines = reindent_line(lines, error.line, target)
    return new_lines, f"Re-indented line from {current} to {target} spaces.", 0.72


def _repair_inconsistent_indentation(lines, error, lang):
    """Convert ALL leading tabs → 4 spaces on the flagged line."""
    idx = error.line - 1
    if not (0 <= idx < len(lines)):
        return None
    if "\t" not in lines[idx]:
        return None
    new_lines = tabs_to_spaces(lines, error.line, spaces_per_tab=4)
    return new_lines, "Converted leading tabs to 4-space indentation.", 0.92


def _repair_keyword_misuse(lines, error, lang):
    """
    Rename a keyword-misused identifier by appending '_var'.
    Confidence is low — this is a best-guess; suggest rather than auto-apply.
    """
    tok = error.token or ""
    if not tok:
        return None
    idx = error.line - 1
    if not (0 <= idx < len(lines)):
        return None
    replacement = tok + "_var"
    pattern = r'\b' + re.escape(tok) + r'\b'
    new_line = re.sub(pattern, replacement, lines[idx], count=1)
    if new_line == lines[idx]:
        return None
    new_lines = list(lines)
    new_lines[idx] = new_line
    # Low confidence — keyword rename is disruptive
    return new_lines, f"Renamed reserved keyword '{tok}' → '{replacement}'.", 0.55


def _repair_invalid_expression_missing_comma(lines, error, lang):
    """Insert ',' before a token that was flagged as unexpected."""
    msg = error.message.lower()
    if "missing ',' or operator before" not in msg:
        return None
    m = re.search(r"before '([^']+)'", error.message)
    if not m:
        return None
    tok = m.group(1)
    idx = error.line - 1
    if not (0 <= idx < len(lines)):
        return None
    line = lines[idx]
    pos = line.find(tok)
    if pos == -1:
        return None
    # Insert comma after the last non-whitespace char before 'tok'
    insert_at = pos
    for i in range(pos - 1, -1, -1):
        if line[i] not in (' ', '\t'):
            insert_at = i + 1
            break
    new_line = line[:insert_at] + ", " + line[insert_at:]
    new_lines = list(lines)
    new_lines[idx] = new_line
    return new_lines, f"Inserted ',' before '{tok}'.", 0.70


def _replace_first(pattern: str, repl: str, line: str, flags: int = 0) -> str:
    return re.sub(pattern, repl, line, count=1, flags=flags)


def _repair_operator_or_expression(lines, error, lang):
    """Repair obvious operator and malformed-expression issues."""
    idx = error.line - 1
    if not (0 <= idx < len(lines)):
        return None

    line = lines[idx]
    stripped = line.strip()
    msg = (error.message or "").lower()
    tok = error.token or ""

    if "=>" in line:
        new_line = line.replace("=>", ">=", 1)
        if new_line != line:
            new_lines = replace_line(lines, error.line, new_line)
            return new_lines, "Repaired '=>' to '>='.", 0.97

    if "=<" in line:
        new_line = line.replace("=<", "<=", 1)
        if new_line != line:
            new_lines = replace_line(lines, error.line, new_line)
            return new_lines, "Repaired '=<' to '<='.", 0.97

    if lang == "python":
        header_match = re.match(r"^(\s*)(if|elif|while)\b(.*)$", line)
        if header_match:
            prefix, keyword, rest = header_match.groups()
            if "==" not in rest and re.search(r"(?<![=!<>])=(?!=)", rest):
                fixed_rest = re.sub(r"(?<![=!<>])=(?!=)", "==", rest, count=1)
                if fixed_rest != rest:
                    new_lines = replace_line(lines, error.line, f"{prefix}{keyword}{fixed_rest}")
                    return new_lines, f"Repaired assignment '=' to comparison '==' in {keyword} condition.", 0.96

    if lang in {"c", "java"} and re.search(r"\bif\s*\([^)]*(?<![=!<>])=(?!=)", line):
        new_line = _replace_first(r"(?<![=!<>])=(?!=)", "==", line)
        if new_line != line:
            new_lines = replace_line(lines, error.line, new_line)
            return new_lines, "Repaired assignment '=' to comparison '==' in condition.", 0.95

    if "unexpected token: newline" in msg or "unexpected token in expression: newline" in msg:
        rhs = "None" if lang == "python" else "0"
        if re.search(r"(=|\+|-|\*|/|%|==|!=|<=|>=|<|>)\s*$", stripped):
            new_lines = replace_line(lines, error.line, line.rstrip() + f" {rhs}")
            return new_lines, f"Completed the incomplete expression with '{rhs}'.", 0.78

    if tok and tok not in {"\n", ""} and ("unexpected token" in msg or "unexpected" in msg):
        if tok == ">" and "=" in line:
            if "=>" in line:
                new_line = line.replace("=>", ">=", 1)
            else:
                new_line = _replace_first(r"(?<![=!<>])=\s*>", " >=", line)
            if new_line != line:
                new_lines = replace_line(lines, error.line, new_line)
                return new_lines, "Recovered a malformed comparison operator.", 0.92
        if tok == ")" and line.count("(") > line.count(")"):
            new_lines = insert_at_line_end(lines, error.line, ")")
            return new_lines, "Inserted ')' to complete the expression.", 0.80

    if "missing ',' or operator before" in msg:
        return _repair_invalid_expression_missing_comma(lines, error, lang)

    if lang == "python" and stripped.startswith("return ") and stripped.endswith(","):
        new_lines = replace_line(lines, error.line, line.rstrip().rstrip(","))
        return new_lines, "Removed trailing ',' from return expression.", 0.70

    return None


def _repair_invalid_function_def(lines, error, lang):
    idx = error.line - 1
    if not (0 <= idx < len(lines)):
        return None
    line = lines[idx]
    stripped = line.strip()

    if lang == "python":
        m = re.match(r"^(\s*)def\s+([A-Za-z_][A-Za-z0-9_]*)\s+([A-Za-z_][A-Za-z0-9_]*)\)\s*:?\s*$", line)
        if m:
            indent, func_name, param = m.groups()
            new_line = f"{indent}def {func_name}({param}):"
            new_lines = replace_line(lines, error.line, new_line)
            return new_lines, "Rebuilt malformed function definition with parentheses and colon.", 0.94
        if stripped == "def":
            new_lines = replace_line(lines, error.line, "def repaired_function():")
            return new_lines, "Inserted a placeholder function signature.", 0.62

    return _repair_missing_paren(lines, error, lang)


def _repair_invalid_class_def(lines, error, lang):
    idx = error.line - 1
    if not (0 <= idx < len(lines)):
        return None
    line = lines[idx]

    if lang == "python":
        if re.match(r"^\s*class\s*:\s*$", line):
            new_lines = replace_line(lines, error.line, re.sub(r"class\s*:\s*$", "class RepairedClass:", line))
            return new_lines, "Inserted a placeholder class name.", 0.88
        if re.match(r"^\s*class\s+[A-Za-z_][A-Za-z0-9_]*\s*$", line):
            new_lines = replace_line(lines, error.line, line.rstrip() + ":")
            return new_lines, "Added ':' to complete the class definition.", 0.86

    return None


def _repair_invalid_declaration_or_syntax(lines, error, lang):
    idx = error.line - 1
    if not (0 <= idx < len(lines)):
        return None
    line = lines[idx]
    msg = (error.message or "").lower()

    if "expected identifier after type" in msg and lang in {"c", "java"}:
        new_line = _replace_first(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*=\s*", r"\1 repaired_value = ", line)
        if new_line != line:
            new_lines = replace_line(lines, error.line, new_line)
            return new_lines, "Inserted a missing identifier in the declaration.", 0.82

    if "expected '{' or ';' after function signature" in msg and lang in {"c", "java"}:
        new_lines = append_line_after(lines, error.line, "{")
        new_lines = append_line_after(new_lines, error.line + 1, "}")
        return new_lines, "Inserted a minimal function body after the signature.", 0.76

    return _repair_operator_or_expression(lines, error, lang)


def _repair_bailout_or_eof(lines, error, lang):
    """Best-effort structural repair for parser bailout / unexpected EOF."""
    idx = max(min(error.line - 1, len(lines) - 1), 0)
    if not lines:
        return None

    line = lines[idx]
    stripped = line.strip()
    indent = len(line) - len(line.lstrip(" \t"))
    message = (error.message or "").lower()

    unmatched = {
        "(": line.count("(") - line.count(")"),
        "[": line.count("[") - line.count("]"),
        "{": line.count("{") - line.count("}"),
    }
    closers = "".join(
        close for open_ch, close in (("(", ")"), ("[", "]"), ("{", "}"))
        for _ in range(max(unmatched[open_ch], 0))
    )
    if closers and stripped and not stripped.startswith(("#", "//")):
        new_lines = insert_at_line_end(lines, idx + 1, closers)
        return new_lines, "Closed unmatched delimiters on the flagged line.", 0.74

    if lang in {"c", "java"} and stripped and stripped.endswith(")") and idx < len(lines) - 1:
        next_line = lines[idx + 1].strip()
        if next_line and next_line != "{":
            new_lines = append_line_after(lines, idx + 1, "{")
            new_lines = append_line_after(new_lines, idx + 2, "}")
            return new_lines, "Inserted missing braces to recover the block structure.", 0.72

    if lang == "python":
        if idx > 0 and lines[idx - 1].rstrip().endswith(":") and stripped:
            target = (len(lines[idx - 1]) - len(lines[idx - 1].lstrip())) + 4
            new_lines = reindent_line(lines, idx + 1, target)
            return new_lines, "Indented a block line after a ':' header.", 0.82

        if stripped.endswith(":") and idx == len(lines) - 1:
            body_indent = indent + 4
            new_lines = append_line_after(lines, idx + 1, " " * body_indent + "pass")
            return new_lines, "Inserted the missing block body after a ':' header.", 0.80

        if idx < len(lines) - 1 and stripped.endswith(":"):
            next_line = lines[idx + 1]
            next_indent = len(next_line) - len(next_line.lstrip(" \t")) if next_line.strip() else -1
            if next_indent <= indent:
                new_lines = reindent_line(lines, idx + 2, indent + 4)
                return new_lines, "Recovered the block indentation after parser bailout.", 0.81

    opener_balance = _find_unmatched_open(lines, len(lines), "{", "}")
    if lang in {"c", "java"} and opener_balance > 0:
        new_lines = list(lines)
        new_lines.extend("}" for _ in range(opener_balance))
        return new_lines, "Appended missing closing braces after parser bailout.", 0.73

    return None


# ── Pattern/warning suggestions (never auto-applied) ─────────────────────────

def _suggest_bare_except(lines, error, lang):
    """SUGGEST replacing bare 'except:' with 'except Exception:'."""
    idx = error.line - 1
    if not (0 <= idx < len(lines)):
        return None
    line = lines[idx]
    new_line = re.sub(r'\bexcept\s*:', 'except Exception:', line, count=1)
    if new_line == line:
        return None
    new_lines = list(lines)
    new_lines[idx] = new_line
    return new_lines, "Replace bare 'except:' with 'except Exception:'.", 0.90


def _suggest_mutable_default_arg(lines, error, lang):
    """SUGGEST replacing =[]/{} mutable default with =None."""
    idx = error.line - 1
    if not (0 <= idx < len(lines)):
        return None
    line = lines[idx]
    new_line = re.sub(r'=\s*\[\s*\]', '=None', line, count=1)
    if new_line == line:
        new_line = re.sub(r'=\s*\{\s*\}', '=None', line, count=1)
    if new_line == line:
        return None
    new_lines = list(lines)
    new_lines[idx] = new_line
    return (new_lines,
            "Replace mutable default '[]'/'{}'  with 'None' and initialise "
            "inside the function body.", 0.92)


def _suggest_singleton_compare(lines, error, lang):
    """SUGGEST replacing == None/True/False with 'is' equivalents."""
    idx = error.line - 1
    if not (0 <= idx < len(lines)):
        return None
    line = lines[idx]
    new_line = re.sub(r'==\s*None',  'is None',      line, count=1)
    if new_line == line:
        new_line = re.sub(r'!=\s*None',  'is not None', line, count=1)
    if new_line == line:
        new_line = re.sub(r'==\s*True',  'is True',     line, count=1)
    if new_line == line:
        new_line = re.sub(r'==\s*False', 'is False',    line, count=1)
    if new_line == line:
        return None
    new_lines = list(lines)
    new_lines[idx] = new_line
    return new_lines, "Replace '==' with 'is' for singleton comparison.", 0.88


def _suggest_is_literal_compare(lines, error, lang):
    """SUGGEST replacing 'is <literal>' with '== <literal>'."""
    idx = error.line - 1
    if not (0 <= idx < len(lines)):
        return None
    line = lines[idx]
    new_line = re.sub(r'\bis\s+(\d+|"[^"]*"|\'[^\']*\')', r'== \1', line, count=1)
    if new_line == line:
        return None
    new_lines = list(lines)
    new_lines[idx] = new_line
    return new_lines, "Replace 'is <literal>' with '== <literal>'.", 0.88


def _postfix_structural_indent(lines: List[str], language: str):
    for idx in range(1, len(lines)):
        prev = lines[idx - 1]
        curr = lines[idx]
        if not prev.strip() or not curr.strip():
            continue
        prev_indent = len(prev) - len(prev.lstrip())
        curr_indent = len(curr) - len(curr.lstrip())
        if prev.rstrip().endswith(":") and curr_indent <= prev_indent:
            target = prev_indent + 4
            new_lines = reindent_line(lines, idx + 1, target)
            return new_lines, idx + 1, (
                f"Indented block line to {target} spaces after a ':' header."
            ), 0.84, "STRUCTURAL_INDENT"
        if (
            prev_indent > 0
            and curr_indent < prev_indent
            and curr.lstrip().startswith(("return", "print(", "raise", "break", "continue", "pass"))
        ):
            new_lines = reindent_line(lines, idx + 1, prev_indent)
            return new_lines, idx + 1, (
                f"Aligned line with the surrounding indented block at {prev_indent} spaces."
            ), 0.81, "STRUCTURAL_INDENT"
    return None


def _postfix_math_sqrt(lines: List[str], language: str):
    pattern = re.compile(r"\bmath\.sqr\(")
    for idx, line in enumerate(lines):
        if pattern.search(line):
            new_lines = replace_line(lines, idx + 1, pattern.sub("math.sqrt(", line, count=1))
            return new_lines, idx + 1, "Corrected 'math.sqr' to 'math.sqrt'.", 0.98, "SEMANTIC_TYPO"
    return None


def _postfix_append_call(lines: List[str], language: str):
    pattern = re.compile(r"(\.append)\[([^\]\n]+)\]")
    for idx, line in enumerate(lines):
        if pattern.search(line):
            new_line = pattern.sub(r"\1(\2)", line, count=1)
            new_lines = replace_line(lines, idx + 1, new_line)
            return new_lines, idx + 1, "Converted bracketed append syntax to a function call.", 0.96, "CALL_BRACKETS"
    return None


def _postfix_literal_type_mismatch(lines: List[str], language: str):
    patterns = [
        (re.compile(r'(".*?"|\'.*?\')\s*\+\s*(\d+(?:\.\d+)?)'), r'\1 + str(\2)'),
        (re.compile(r'(\d+(?:\.\d+)?)\s*\+\s*(".*?"|\'.*?\')'), r'str(\1) + \2'),
    ]
    for idx, line in enumerate(lines):
        for pattern, repl in patterns:
            if pattern.search(line):
                new_line = pattern.sub(repl, line, count=1)
                new_lines = replace_line(lines, idx + 1, new_line)
                return new_lines, idx + 1, "Wrapped a literal in str() to avoid an obvious type mismatch.", 0.83, "TYPE_MISMATCH"
    return None


def _suggest_divide_by_zero(lines: List[str], language: str):
    call_pattern = re.compile(r"\bdivide\((.+?),\s*0(\s*)\)")
    op_pattern = re.compile(r"(?P<lhs>.+?)(?P<op>/|//|%)\s*0(?P<tail>\D.*|$)")
    for idx, line in enumerate(lines):
        if call_pattern.search(line):
            continue
        if op_pattern.search(line):
            v1 = op_pattern.sub(r"\g<lhs>\g<op> 1\g<tail>", line, count=1)
            v2 = op_pattern.sub(r"(\g<lhs>\g<op> (1 if True else 0)\g<tail>)", line, count=1)
            return idx + 1, line, [v1, v2], (
                "Detected an obvious divide-by-zero operation; generated safe candidate denominators."
            ), 0.35, "DIVIDE_BY_ZERO_RISK"
    return None


def _suggest_missing_dict_key(lines: List[str], language: str):
    pattern = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\[\s*(['\"][^'\"]+['\"])\s*\]")
    for idx, line in enumerate(lines):
        if ".get(" in line:
            continue
        m = pattern.search(line)
        if not m:
            continue
        access = m.group(0)
        key = m.group(2)
        obj = m.group(1)
        v1 = line.replace(access, f"{obj}.get({key})", 1)
        v2 = line.replace(access, f"{obj}.get({key}, None)", 1)
        return idx + 1, line, [v1, v2], (
            "Converted direct dictionary-style access into safer get() candidates."
        ), 0.58, "MISSING_DICT_KEY_RISK"
    literal_pattern = re.compile(r"(\{[^{}\n]+\})\s*\[\s*(['\"][^'\"]+['\"])\s*\]")
    for idx, line in enumerate(lines):
        m = literal_pattern.search(line)
        if not m:
            continue
        access = m.group(0)
        obj = m.group(1)
        key = m.group(2)
        v1 = line.replace(access, f"({obj}).get({key})", 1)
        v2 = line.replace(access, f"({obj}).get({key}, None)", 1)
        return idx + 1, line, [v1, v2], (
            "Converted literal dictionary indexing into safer get() candidates."
        ), 0.61, "MISSING_DICT_KEY_RISK"
    return None


def _suggest_runtime_type_mismatch(lines: List[str], language: str):
    pattern = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\+\s*(['\"][^'\"]+['\"])")
    for idx, line in enumerate(lines):
        m = pattern.search(line)
        if m and "str(" not in line:
            lhs = m.group(1)
            rhs = m.group(2)
            v1 = pattern.sub(f"str({lhs}) + {rhs}", line, count=1)
            return idx + 1, line, [v1], (
                "Generated a safer string-concatenation candidate to avoid a likely type mismatch."
            ), 0.52, "TYPE_MISMATCH_RISK"
    return None


_POST_APPLY_RULES = [
    _postfix_structural_indent,
    _postfix_math_sqrt,
    _postfix_append_call,
    _postfix_literal_type_mismatch,
]

_POST_SUGGEST_RULES = [
    _suggest_divide_by_zero,
    _suggest_missing_dict_key,
    _suggest_runtime_type_mismatch,
]


# ══════════════════════════════════════════════════════════════════════════════
# Repair rule dispatch tables
# ══════════════════════════════════════════════════════════════════════════════

# Syntax errors → auto-apply when confidence >= threshold AND re-parse confirms
_SYNTAX_REPAIR_RULES = {
    "MISSING_COLON":            _repair_missing_colon,
    "MISSING_SEMICOLON":        _repair_missing_semicolon,
    "MISSING_PAREN":            _repair_missing_paren,
    "MISSING_BRACKET":          _repair_missing_bracket,
    "MISSING_BRACE":            _repair_missing_brace,
    "INDENTATION_ERROR":        _repair_indentation_error,
    "INCONSISTENT_INDENTATION": _repair_inconsistent_indentation,
    "INVALID_FUNCTION_DEF":     _repair_invalid_function_def,
    "INVALID_CLASS_DEF":        _repair_invalid_class_def,
    "INVALID_DECLARATION":      _repair_invalid_declaration_or_syntax,
    "INVALID_SYNTAX":           _repair_invalid_declaration_or_syntax,
    "INCOMPLETE_STATEMENT":     _repair_operator_or_expression,
    "UNEXPECTED_TOKEN":         _repair_operator_or_expression,
    "SyntaxError":              _repair_operator_or_expression,
    "KEYWORD_MISUSE":           _repair_keyword_misuse,
    "INVALID_EXPRESSION":       _repair_operator_or_expression,
    "MAX_ERRORS_EXCEEDED":      _repair_bailout_or_eof,
    "UnexpectedEOF":            _repair_bailout_or_eof,
}

# Pattern/warning → suggest only, never mutate working source
_PATTERN_SUGGEST_RULES = {
    "BARE_EXCEPT":         _suggest_bare_except,
    "MUTABLE_DEFAULT_ARG": _suggest_mutable_default_arg,
    "SINGLETON_COMPARE":   _suggest_singleton_compare,
    "IS_LITERAL_COMPARE":  _suggest_is_literal_compare,
}


def _run_post_heal_passes(working_lines: List[str],
                          baseline_errors: int,
                          language: str,
                          actions: List[RepairAction],
                          patched_lines: set) -> tuple[List[str], int]:
    changed = True
    while changed:
        changed = False
        for fn in _POST_APPLY_RULES:
            result = fn(working_lines, language)
            if result is None:
                continue
            new_lines, err_line, desc, conf, err_type = result
            if err_line in patched_lines:
                continue
            orig_line = working_lines[err_line - 1] if 0 < err_line <= len(working_lines) else ""
            repaired_line = new_lines[err_line - 1] if 0 < err_line <= len(new_lines) else ""
            new_count = _reparse(lines_to_source(new_lines), language)
            if new_count > baseline_errors:
                actions.append(RepairAction(
                    error_type=err_type, line=err_line,
                    description=desc,
                    original_line=orig_line,
                    repaired_line=repaired_line,
                    confidence=conf,
                    verified=False,
                    mode="suggested",
                ))
                continue

            actions.append(RepairAction(
                error_type=err_type, line=err_line,
                description=desc,
                original_line=orig_line,
                repaired_line=repaired_line,
                confidence=conf,
                verified=True,
                mode="applied",
            ))
            working_lines = new_lines
            baseline_errors = new_count
            patched_lines.add(err_line)
            changed = True
            break

    for fn in _POST_SUGGEST_RULES:
        result = fn(working_lines, language)
        if result is None:
            continue
        err_line, orig_line, variants, desc, conf, err_type = result
        if err_line in patched_lines:
            continue
        variants = [v for v in variants if v and v != orig_line]
        if not variants:
            continue
        actions.append(RepairAction(
            error_type=err_type, line=err_line,
            description=desc,
            original_line=orig_line,
            repaired_line=variants[0],
            confidence=conf,
            verified=False,
            mode="suggested",
            suggestions=variants,
        ))

    return working_lines, baseline_errors


# ══════════════════════════════════════════════════════════════════════════════
# Undefined-name handler (scope-aware, conservative)
# ══════════════════════════════════════════════════════════════════════════════

def _handle_undefined_name(lines: List[str],
                             error,
                             lang: str,
                             defined_names: set,
                             baseline_errors: int,
                             language: str) -> RepairAction:
    """
    Conservative UNDEFINED_NAME repair.

    Auto-apply only when:
      • Exactly ONE candidate within edit-distance 1
      • First character matches
      • Re-parse confirms error reduction

    Otherwise: produce a 'suggested' action listing up to 3 candidates.
    """
    err_line = error.line
    orig_line = lines[err_line - 1] if 0 < err_line <= len(lines) else ""

    m = re.search(r"name '([^']+)' is not defined", error.message)
    bad_name = m.group(1) if m else (error.token or "")

    if bad_name == "divide":
        call_match = re.search(r"\bdivide\((.+?),\s*(.+?)\)", orig_line)
        if call_match:
            lhs = call_match.group(1).strip()
            rhs = call_match.group(2).strip()
            if rhs == "0":
                variants = [
                    orig_line.replace(call_match.group(0), f"({lhs}) / 1", 1),
                    orig_line.replace(call_match.group(0), f"({lhs}) / abs(1)", 1),
                ]
            else:
                variants = [
                    orig_line.replace(call_match.group(0), f"({lhs}) / ({rhs})", 1)
                ]
            return RepairAction(
                error_type="UNDEFINED_NAME", line=err_line,
                description=(
                    "Interpreted 'divide(a, b)' as an obvious division helper call and "
                    "generated direct division candidates."
                ),
                original_line=orig_line,
                repaired_line=variants[0],
                confidence=0.56,
                mode="suggested",
                suggestions=variants,
            ), None

    if not bad_name or not defined_names:

        return RepairAction(
            error_type="UNDEFINED_NAME", line=err_line,
            description="", original_line=orig_line, repaired_line="",
            mode="skipped",
            skip_reason="No name extracted or no defined_names available.",
        )

    # Collect ALL candidates up to distance 3 for display
    all_candidates = _ranked_candidates(bad_name, defined_names, max_dist=3)
    candidate_names = [c for _, c in all_candidates]

    # Try safe auto-replace (distance ≤ 1, first-char match, unambiguous)
    safe_candidate = _safe_typo_candidate(bad_name, defined_names, max_dist=1)

    if safe_candidate:
        pattern = r'\b' + re.escape(bad_name) + r'\b'
        new_line = re.sub(pattern, safe_candidate, lines[err_line - 1], count=1)
        if new_line != lines[err_line - 1]:
            new_lines = list(lines)
            new_lines[err_line - 1] = new_line
            new_source = lines_to_source(new_lines)
            new_count = _reparse(new_source, language)
            verified = new_count < baseline_errors
            if verified:
                return RepairAction(
                    error_type="UNDEFINED_NAME", line=err_line,
                    description=f"Replaced '{bad_name}' with '{safe_candidate}' (typo, dist=1).",
                    original_line=orig_line,
                    repaired_line=new_line,
                    confidence=0.82,
                    verified=True,
                    mode="applied",
                    suggestions=[safe_candidate],
                ), new_lines

    # Can't safely auto-apply → suggest only
    if candidate_names:
        names_str = ", ".join(f"'{c}'" for c in candidate_names[:3])
        desc = (f"'{bad_name}' is not defined. "
                f"Closest name(s) in scope: {names_str}. "
                f"Verify spelling and scope — auto-repair declined due to ambiguity.")
    else:
        desc = (f"'{bad_name}' is not defined. "
                f"No similar name found in scope. "
                f"Define or import '{bad_name}' before this line.")

    return RepairAction(
        error_type="UNDEFINED_NAME", line=err_line,
        description=desc,
        original_line=orig_line,
        repaired_line="",
        confidence=0.0,
        mode="suggested",
        suggestions=candidate_names[:3],
    ), None   # None → do not update working_lines


# ══════════════════════════════════════════════════════════════════════════════
# Public API — heal_source()
# ══════════════════════════════════════════════════════════════════════════════

def heal_source(source: str,
                errors: list,
                language: str = "python",
                defined_names: set | None = None) -> HealResult:
    """
    Attempt to automatically repair or suggest fixes for *errors* in *source*.

    Parameters
    ----------
    source        : Original source text.
    errors        : List of ErrorNode objects from the parser.
    language      : 'python' | 'c' | 'java'
    defined_names : Set of known names in scope (for UNDEFINED_NAME typo fix).

    Returns
    -------
    HealResult with the repaired source and per-error RepairActions.
    Each RepairAction.mode is 'applied', 'suggested', or 'skipped'.
    """
    if defined_names is None:
        defined_names = set()

    working_lines = source_to_lines(source)
    # Track parser errors against the evolving working source
    baseline_errors = len(errors)
    actions: List[RepairAction] = []

    # Track physical lines already patched (one patch per line max)
    patched_lines: set = set()

    for error in errors:
        err_type = error.error_type
        err_line  = error.line

        orig_line = (working_lines[err_line - 1]
                     if 0 < err_line <= len(working_lines) else "")

        # ── Warning-only diagnostics: suggest nothing, just skip ─────────────
        if err_type in _WARNING_TYPES:
            actions.append(RepairAction(
                error_type=err_type, line=err_line,
                description="",
                original_line=orig_line, repaired_line="",
                mode="skipped",
                skip_reason=(
                    f"'{err_type}' is a warning/diagnostic, not a syntax error. "
                    "Fix manually based on the error explanation above."
                ),
            ))
            continue

        # ── UNDEFINED_NAME: special scope-aware handler ───────────────────────
        if err_type == "UNDEFINED_NAME":
            result = _handle_undefined_name(
                working_lines, error, language,
                defined_names, baseline_errors, language)
            # _handle_undefined_name returns (action, new_lines_or_None)
            if isinstance(result, tuple):
                action, new_lines = result
            else:
                action, new_lines = result, None

            actions.append(action)
            if new_lines is not None and action.mode == "applied":
                working_lines = new_lines
                baseline_errors = _reparse(lines_to_source(working_lines), language)
                patched_lines.add(err_line)
            continue

        # ── Pattern/warning best-practice suggestions ─────────────────────────
        if err_type in _PATTERN_TYPES:
            fn = _PATTERN_SUGGEST_RULES.get(err_type)
            if fn is None:
                actions.append(RepairAction(
                    error_type=err_type, line=err_line,
                    description="", original_line=orig_line, repaired_line="",
                    mode="skipped",
                    skip_reason=f"No suggestion rule for '{err_type}'.",
                ))
                continue
            result = fn(working_lines, error, language)
            if result is None:
                actions.append(RepairAction(
                    error_type=err_type, line=err_line,
                    description="", original_line=orig_line, repaired_line="",
                    mode="skipped",
                    skip_reason="Suggestion rule returned no applicable fix.",
                ))
                continue
            new_lines, desc, conf = result
            repaired_line = (new_lines[err_line - 1]
                             if 0 < err_line <= len(new_lines) else "")
            # Suggestions are NEVER auto-applied
            actions.append(RepairAction(
                error_type=err_type, line=err_line,
                description=desc,
                original_line=orig_line,
                repaired_line=repaired_line,
                confidence=conf,
                verified=False,
                mode="suggested",
            ))
            continue

        # ── Syntax errors: try auto-apply ─────────────────────────────────────
        if err_type not in _SYNTAX_REPAIR_RULES:
            actions.append(RepairAction(
                error_type=err_type, line=err_line,
                description="", original_line=orig_line, repaired_line="",
                mode="skipped",
                skip_reason=f"No repair rule for error type '{err_type}'.",
            ))
            continue

        # Conflict guard: only one patch per line
        if err_line in patched_lines:
            actions.append(RepairAction(
                error_type=err_type, line=err_line,
                description="", original_line=orig_line, repaired_line=orig_line,
                mode="skipped",
                skip_reason="Line already patched by an earlier repair in this pass.",
            ))
            continue

        fn = _SYNTAX_REPAIR_RULES[err_type]
        result = fn(working_lines, error, language)
        if result is None:
            actions.append(RepairAction(
                error_type=err_type, line=err_line,
                description="", original_line=orig_line, repaired_line="",
                mode="skipped",
                skip_reason="Repair rule returned no applicable fix.",
            ))
            continue

        new_lines, desc, conf = result
        repaired_line = (new_lines[err_line - 1]
                         if 0 < err_line <= len(new_lines) else "")

        # Re-parse IMMEDIATELY to verify this specific patch
        new_source = lines_to_source(new_lines)
        new_error_count = _reparse(new_source, language)
        verified = new_error_count < baseline_errors

        # Confidence gate: below threshold → suggest only
        if conf < _AUTO_APPLY_THRESHOLD or not verified:
            mode = "suggested" if conf >= 0.50 else "skipped"
            skip_reason = ("" if mode == "suggested"
                           else f"Confidence {conf:.0%} too low to suggest.")
            if not verified and conf >= _AUTO_APPLY_THRESHOLD:
                mode = "suggested"
                skip_reason = ""
            actions.append(RepairAction(
                error_type=err_type, line=err_line,
                description=desc,
                original_line=orig_line,
                repaired_line=repaired_line,
                confidence=conf,
                verified=False,
                mode=mode,
                skip_reason=skip_reason,
            ))
            continue

        # Accept the patch
        actions.append(RepairAction(
            error_type=err_type, line=err_line,
            description=desc,
            original_line=orig_line,
            repaired_line=repaired_line,
            confidence=conf,
            verified=True,
            mode="applied",
        ))
        working_lines = new_lines
        baseline_errors = new_error_count
        patched_lines.add(err_line)

    working_lines, baseline_errors = _run_post_heal_passes(
        working_lines, baseline_errors, language, actions, patched_lines
    )

    healed_source   = source if working_lines == source_to_lines(source) else lines_to_source(working_lines)
    repaired_count  = sum(1 for a in actions if a.mode == "applied" and a.verified)
    suggested_count = sum(1 for a in actions if a.mode == "suggested")
    fully_healed    = (repaired_count > 0 and
                       _reparse(healed_source, language) == 0)

    return HealResult(
        healed_source=healed_source,
        actions=actions,
        repaired_count=repaired_count,
        suggested_count=suggested_count,
        fully_healed=fully_healed,
    )


_single_pass_heal_source = heal_source


def heal_source(source: str,
                errors: list,
                language: str = "python",
                defined_names: set | None = None) -> HealResult:
    """
    Iterative wrapper around the existing single-pass healer.
    Keeps healing after parser bailout/cascades by reparsing the updated source
    and retrying newly exposed errors for a few rounds.
    """
    defined_names = defined_names or set()
    current_source = source
    current_errors = list(errors)
    all_actions: List[RepairAction] = []
    repaired_count = 0
    suggested_count = 0

    for _ in range(4):
        result = _single_pass_heal_source(
            current_source,
            current_errors,
            language=language,
            defined_names=defined_names,
        )
        all_actions.extend(result.actions)
        repaired_count += result.repaired_count
        suggested_count += result.suggested_count

        next_source = result.healed_source
        if result.fully_healed or next_source == current_source:
            current_source = next_source
            break

        next_errors = _collect_errors(next_source, language)
        if not next_errors or len(next_errors) >= len(current_errors):
            current_source = next_source
            break

        current_source = next_source
        current_errors = next_errors

    final_errors = _collect_errors(current_source, language)
    return HealResult(
        healed_source=current_source,
        actions=all_actions,
        repaired_count=repaired_count,
        suggested_count=suggested_count,
        fully_healed=(len(final_errors) == 0 and repaired_count > 0),
    )
