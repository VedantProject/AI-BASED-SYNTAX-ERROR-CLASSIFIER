"""
analyze_code.py -- Syntax Error Analyzer
========================================
Supports Python (rule-based classification + optional ML severity),
C, and Java (parser + rule-based fixes).

Architecture
------------
  Detection   : language parsers (parsers/)
  Classification : rule-based table keyed on ErrorNode.error_type
  Fix suggestions: rule-based generator, uses difflib for NameError hints
  Severity    : rule-based score table; ML severity regressor used when
                models are available (Python only, as supplementary signal)

Usage:
    python analyze_code.py myfile.py        # Python file
    python analyze_code.py myfile.c         # C file
    python analyze_code.py MyClass.java     # Java file
    python analyze_code.py                  # interactive paste mode
    python analyze_code.py --lang c         # force language
    cat file.py | python analyze_code.py    # piped input
"""

from __future__ import annotations

import difflib
import os
import re
import sys
import textwrap
import time
from collections import defaultdict
from types import SimpleNamespace
from typing import List, Tuple

# ── Add project root so all imports resolve ───────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── Ensure UTF-8 output on Windows; fall back to ASCII art if needed ──────────
def _configure_output() -> bool:
    """
    Switch stdout to UTF-8 and probe whether box-drawing characters can be
    written.  Returns True for Unicode mode, False for plain-ASCII fallback.
    """
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        else:
            import io
            sys.stdout = io.TextIOWrapper(
                sys.stdout.buffer, encoding='utf-8',
                errors='replace', line_buffering=True)
    except Exception:
        return False  # could not reconfigure at all

    # Verify the terminal can actually encode a box-drawing char
    try:
        probe = '═'.encode(sys.stdout.encoding or 'utf-8')
        return probe != b'?'  # 'replace' gives '?' when encoding fails
    except Exception:
        return True   # encoding succeeded without error

_UNICODE_OK = _configure_output()

# ── Display helpers ───────────────────────────────────────────────────────────

# Box-drawing constants: Unicode when supported, plain ASCII fallback
if _UNICODE_OK:
    BORDER = "═" * 70          # ══════...
    THIN   = "─" * 70          # ──────...
    HALF   = "─" * 50          # ──────...
    _BOX_TL  = "┌"             # ┌
    _BOX_VT  = "│"             # │
    _BOX_BL  = "└"             # └
    _BOX_H   = "─"             # ─
    _ARROW   = "└──" # └──
    _TICK    = "✓"             # ✓
    _CROSS   = "✗"             # ✗
    _INFO    = "ℹ"             # ℹ
    _WRENCH  = "🔧"         # 🔧
else:
    BORDER = "=" * 70
    THIN   = "-" * 70
    HALF   = "-" * 50
    _BOX_TL  = "+"
    _BOX_VT  = "|"
    _BOX_BL  = "+"
    _BOX_H   = "-"
    _ARROW   = "+--"
    _TICK    = "OK"
    _CROSS   = "!!"
    _INFO    = "i"
    _WRENCH  = "[*]"

# Override display symbols with ASCII-safe source literals so output does not
# depend on how this file itself was decoded.
if _UNICODE_OK:
    BORDER = "\u2550" * 70
    THIN = "\u2500" * 70
    HALF = "\u2500" * 50
    _BOX_TL = "\u250c"
    _BOX_VT = "\u2502"
    _BOX_BL = "\u2514"
    _BOX_H = "\u2500"
    _ARROW = "\u2514\u2500\u2500"
    _TICK = "\u2713"
    _CROSS = "\u2717"
    _INFO = "\u2139"
else:
    BORDER = "=" * 70
    THIN = "-" * 70
    HALF = "-" * 50
    _BOX_TL = "+"
    _BOX_VT = "|"
    _BOX_BL = "+"
    _BOX_H = "-"
    _ARROW = "+--"
    _TICK = "OK"
    _CROSS = "!!"
    _INFO = "i"


def _section_title(title: str) -> str:
    return f"  {_BOX_TL}{_BOX_H} {title} "


def _diagnostic_kind(error_type: str, py_class: str) -> str:
    if error_type in {
        "MISSING_RETURN",
        "UNUSED_VARIABLE",
        "REDUNDANT_ASSIGNMENT",
        "MUTABLE_DEFAULT_ARG",
        "BARE_EXCEPT",
        "EMPTY_EXCEPT",
        "IS_LITERAL_COMPARE",
        "SINGLETON_COMPARE",
        "BUILTIN_SHADOW",
        "UNUSED_IMPORT",
    }:
        return "LINT"
    if py_class == "Warning" or error_type in {"UNREACHABLE_CODE", "INFINITE_LOOP"}:
        return "WARNING"
    return "ERROR"


def _wrap(text: str, width: int = 66, indent: str = "    ") -> str:
    return "\n".join(
        indent + line
        for line in textwrap.fill(text, width).split("\n")
    )



def _bar(confidence: float, width: int = 10) -> str:
    filled = int(round(confidence * width))
    if _UNICODE_OK:
        return "\u2588" * filled + "\u2591" * (width - filled)
    return "#" * filled + "-" * (width - filled)


# ── Levenshtein distance (for typo-aware name suggestions) ───────────────────

def _levenshtein(a: str, b: str) -> int:
    """Compute edit distance between two strings."""
    if a == b:
        return 0
    la, lb = len(a), len(b)
    if la == 0: return lb
    if lb == 0: return la
    prev = list(range(lb + 1))
    for i, ca in enumerate(a, 1):
        curr = [i] + [0] * lb
        for j, cb in enumerate(b, 1):
            curr[j] = min(
                prev[j] + 1,          # deletion
                curr[j - 1] + 1,      # insertion
                prev[j - 1] + (ca != cb),  # substitution
            )
        prev = curr
    return prev[lb]


def _closest_names(name: str,
                   candidates: set[str],
                   max_dist: int = 3,
                   n: int = 3) -> list[str]:
    """Return up to `n` candidates sorted by Levenshtein distance to `name`.
    Only returns candidates within `max_dist` edits.
    Shorter names get a tiebreak by ratio to avoid suggesting very long names
    for short typos."""
    scored = []
    for c in candidates:
        d = _levenshtein(name.lower(), c.lower())
        # Also require that the candidate shares at least the first character
        # or has a high sequence ratio to avoid wild suggestions
        if d <= max_dist:
            ratio = 1 - d / max(len(name), len(c), 1)
            scored.append((d, -ratio, c))
    scored.sort()
    return [c for _, _, c in scored[:n]]


# ── Language detection ────────────────────────────────────────────────────────

_EXT_MAP = {
    ".py":   "python",
    ".pyw":  "python",
    ".c":    "c",
    ".h":    "c",
    ".cpp":  "c",
    ".hpp":  "c",
    ".java": "java",
}


def _detect_language(filepath: str) -> str | None:
    _, ext = os.path.splitext(filepath.lower())
    return _EXT_MAP.get(ext)


# ═══════════════════════════════════════════════════════════════════════════
# RULE-BASED ERROR CLASSIFICATION ENGINE
# ═══════════════════════════════════════════════════════════════════════════

# Maps error_type  →  (python_error_class, severity 0-10, short_title, explanation)
_ERROR_RULES: dict[str, tuple[str, int, str, str]] = {
    "MISSING_COLON": (
        "SyntaxError", 8,
        "Missing ':' after block header",
        "Python requires a colon ':' at the end of every compound-statement "
        "header: def, class, if, elif, else, for, while, try, except, with.",
    ),
    "MISSING_PAREN": (
        "SyntaxError", 8,
        "Unmatched or missing parenthesis",
        "Every '(' must have a matching ')'. A missing closer causes the "
        "parser to read past the intended end of the expression.",
    ),
    "MISSING_BRACKET": (
        "SyntaxError", 8,
        "Unmatched or missing bracket",
        "Every '[' must have a matching ']'. This is required for list "
        "literals and subscript operations.",
    ),
    "MISSING_BRACE": (
        "SyntaxError", 8,
        "Unmatched or missing brace",
        "Every '{' must have a matching '}'. This applies to code blocks "
        "(if, for, class, methods in C/Java) and dict/set literals in Python.",
    ),
    "UNMATCHED_DELIMITER": (
        "SyntaxError", 8,
        "Unmatched delimiter",
        "A closing bracket/paren/brace was found with no matching opener, "
        "or an opener was never closed.",
    ),
    "UNDEFINED_NAME": (
        "NameError", 8,
        "Name is not defined",
        "The name was used before being defined, or it is misspelled. "
        "Python looks up names at runtime — a typo here causes a NameError "
        "even if the rest of the code is valid.",
    ),
    "INVALID_EXPRESSION": (
        "SyntaxError", 8,
        "Invalid expression or unexpected token",
        "The parser found a token it did not expect at this position. "
        "Common causes: missing comma between arguments, missing operator, "
        "or a stray keyword.",
    ),
    "INDENTATION_ERROR": (
        "IndentationError", 8,
        "Unexpected indentation level",
        "Python uses indentation to define block scope. This line's indent "
        "does not match the expected level for the enclosing block.",
    ),
    "INCONSISTENT_INDENTATION": (
        "TabError", 8,
        "Mixed tabs and spaces",
        "Python 3 forbids mixing tabs and spaces for indentation. "
        "Use only spaces (4 per level, per PEP 8).",
    ),
    "INCOMPLETE_STATEMENT": (
        "SyntaxError", 6,
        "Incomplete statement",
        "The statement is missing required tokens to be syntactically "
        "complete (e.g., the right-hand side of an assignment).",
    ),
    "INVALID_FUNCTION_DEF": (
        "SyntaxError", 8,
        "Invalid function definition",
        "The function definition is malformed. "
        "Expected format: def name(params):",
    ),
    "INVALID_CLASS_DEF": (
        "SyntaxError", 8,
        "Invalid class definition",
        "The class definition is malformed. "
        "Expected format: class Name: or class Name(Base):",
    ),
    "KEYWORD_MISUSE": (
        "SyntaxError", 8,
        "Reserved keyword used as identifier",
        "A Python reserved keyword (if, for, class, def, …) cannot be used "
        "as a variable or function name.",
    ),
    "INVALID_IMPORT": (
        "SyntaxError", 5,
        "Invalid import statement",
        "The import statement syntax is malformed. "
        "Expected: import module  or  from module import name.",
    ),
    "INVALID_DECORATOR": (
        "SyntaxError", 6,
        "Invalid decorator",
        "The decorator syntax is malformed. Expected: @decorator_name",
    ),
    "SyntaxError": (
        "SyntaxError", 6,
        "Syntax error",
        "The code does not conform to Python syntax rules at this point.",
    ),
    "UnexpectedEOF": (
        "SyntaxError", 9,
        "Unexpected end of file",
        "The file ended before the parser expected. Usually caused by an "
        "unclosed parenthesis, bracket, brace, or string literal.",
    ),
    "MAX_ERRORS_EXCEEDED": (
        "SyntaxError", 5,
        "Too many errors — parsing stopped",
        "Fix the first reported error and re-run. Many false positives "
        "are cascades from a single root cause.",
    ),
    # C / Java specific
    "MISSING_SEMICOLON": (
        "SyntaxError", 7,
        "Missing semicolon",
        "Every statement must be terminated with a semicolon ';'.",
    ),
    "INVALID_DECLARATION": (
        "SyntaxError", 7,
        "Invalid declaration",
        "The declaration syntax is malformed. "
        "Check the type, name, and any modifiers.",
    ),
    "INVALID_SYNTAX": (
        "SyntaxError", 6,
        "Invalid syntax",
        "The statement does not conform to the language grammar.",
    ),
    "INVALID_TYPE": (
        "SyntaxError", 6,
        "Invalid type specifier",
        "The type name is not valid. Check for typos.",
    ),
    "INVALID_MODIFIER": (
        "SyntaxError", 6,
        "Invalid access modifier",
        "Use only valid modifiers (public, private, protected, static, …) "
        "in the correct order.",
    ),
    "INVALID_PREPROCESSOR": (
        "SyntaxError", 7,
        "Invalid preprocessor directive",
        "Check the #include / #define directive syntax and header file path.",
    ),
    "INVALID_PACKAGE": (
        "SyntaxError", 5,
        "Invalid package declaration",
        "The package declaration must appear as the first statement: "
        "package com.example;",
    ),
    # ── Control Flow Analysis ──────────────────────────────────────────────
    "UNREACHABLE_CODE": (
        "Warning", 6,
        "Unreachable code",
        "This code can never be executed because a preceding 'return', "
        "'break', 'continue', or 'raise' statement always exits the block.",
    ),
    "MISSING_RETURN": (
        "Warning", 5,
        "Function missing return on some paths",
        "This function does not explicitly return a value on every code path. "
        "Python implicitly returns None, but this is often unintentional.",
    ),
    "BREAK_OUTSIDE_LOOP": (
        "SyntaxError", 8,
        "'break' outside loop",
        "'break' can only appear inside a 'for' or 'while' loop body.",
    ),
    "CONTINUE_OUTSIDE_LOOP": (
        "SyntaxError", 8,
        "'continue' outside loop",
        "'continue' can only appear inside a 'for' or 'while' loop body.",
    ),
    "INFINITE_LOOP": (
        "Warning", 7,
        "Potential infinite loop",
        "This loop may never terminate. If the condition is always True and "
        "there is no 'break' statement, the program will loop forever.",
    ),
    # ── Data Flow Analysis ─────────────────────────────────────────────────
    "UNUSED_VARIABLE": (
        "Warning", 4,
        "Variable assigned but never used",
        "This variable is assigned a value but is never referenced afterwards. "
        "Consider removing the assignment, or use '_' as the name to signal "
        "intentional discard.",
    ),
    "REDUNDANT_ASSIGNMENT": (
        "Warning", 3,
        "Redundant assignment",
        "This variable is assigned a value that is immediately overwritten by "
        "another assignment without being read in between. The first assignment "
        "has no effect.",
    ),
    # ── Pattern Detection ──────────────────────────────────────────────────
    "MUTABLE_DEFAULT_ARG": (
        "Warning", 7,
        "Mutable default argument",
        "Using a mutable object (list, dict, set) as a default argument is a "
        "common Python pitfall. The same object is shared across all calls that "
        "use the default, so mutations persist between invocations.",
    ),
    "BARE_EXCEPT": (
        "Warning", 6,
        "Bare 'except' clause",
        "A bare 'except:' catches every exception including SystemExit and "
        "KeyboardInterrupt. Always specify the exception type(s) you intend to handle.",
    ),
    "EMPTY_EXCEPT": (
        "Warning", 5,
        "Empty except block",
        "This except block only contains 'pass', silently swallowing exceptions. "
        "At minimum, log the error or re-raise it.",
    ),
    "IS_LITERAL_COMPARE": (
        "Warning", 6,
        "'is' used with a literal value",
        "'is' checks object identity, not value equality. For small integers (-5..256) "
        "CPython caches objects so 'is' may seem to work, but this is an "
        "implementation detail. Use '==' for value comparison.",
    ),
    "SINGLETON_COMPARE": (
        "Warning", 5,
        "Comparison with None/True/False using '=='" ,
        "PEP 8 recommends using 'is' or 'is not' when comparing with the "
        "singletons None, True, and False.",
    ),
    "BUILTIN_SHADOW": (
        "Warning", 6,
        "Built-in name shadowed",
        "Assigning to a built-in name (like 'list', 'str', 'len') hides the "
        "original in the current scope and can cause confusing TypeError / "
        "AttributeError later in the code.",
    ),
    "UNUSED_IMPORT": (
        "Warning", 3,
        "Unused import",
        "This module or name is imported but never referenced in the code. "
        "Unused imports add clutter and slow down startup time.",
    ),
}

_FALLBACK_RULE = (
    "SyntaxError", 5,
    "Syntax error",
    "The code does not conform to the language syntax rules.",
)


def _severity_label(score: int) -> str:
    if score >= 7: return "ERROR"
    if score >= 5: return "WARNING"
    return "INFO"


def classify_error(error_type: str) -> tuple[str, int, str, str]:
    """Return (python_class, severity, title, explanation) for an error_type."""
    return _ERROR_RULES.get(error_type, _FALLBACK_RULE)


# ─── Fix suggestion generator ─────────────────────────────────────────────────

def generate_fixes(error_type: str,
                   message: str,
                   token: str | None,
                   defined_names: set[str]) -> List[str]:
    """
    Returns a list of concrete, human-readable fix strings for an error.
    All logic is rule-based and keyed on error_type + message content.
    """
    msg = message.lower()
    tok = token or ""

    # ── Missing colon ──────────────────────────────────────────────────────
    if error_type == "MISSING_COLON":
        # Determine which keyword the colon follows from the message
        for kw in ("def", "class", "if", "elif", "else", "for",
                   "while", "try", "except", "finally", "with"):
            if kw in msg:
                return [
                    f"Add ':' at the end of the `{kw}` statement header.",
                    f"Correct form: `{kw} ...:` followed by an indented block.",
                ]
        return ["Add ':' at the end of the block header line."]

    # ── Missing paren ──────────────────────────────────────────────────────
    if error_type == "MISSING_PAREN":
        if "function call" in msg or "call" in msg:
            return [
                "Add the missing ')' at the end of the function call.",
                "Check that every '(' inside the arguments also has a ')'.",
            ]
        if "function definition" in msg or "def" in msg:
            return [
                "Add ')' to close the parameter list: `def name(params):`",
            ]
        return [
            "Add the matching closing parenthesis ')'.",
            "Count all '(' in the expression and ensure equal ')' close them.",
        ]

    # ── Missing bracket ────────────────────────────────────────────────────
    if error_type == "MISSING_BRACKET":
        return [
            "Add the matching closing bracket ']'.",
            "Check every list literal `[...]` and subscript `x[...]`.",
        ]

    # ── Missing brace ──────────────────────────────────────────────────────
    if error_type == "MISSING_BRACE":
        return [
            "Add the matching closing brace '}'.",
            "Check every code block (if/for/while/class/method) and dict/set "
            "literal — each opening '{' needs a matching '}'.",
        ]

    # ── Unmatched delimiter ────────────────────────────────────────────────
    if error_type == "UNMATCHED_DELIMITER":
        return [
            f"Check whether '{tok}' has a matching opener or closer.",
            "Use an editor's bracket-match feature to find the mismatch.",
        ]

    # ── Undefined name / NameError ─────────────────────────────────────────
    if error_type == "UNDEFINED_NAME":
        # Extract name from the message produced by our parser
        m = re.search(r"name '([^']+)' is not defined", message)
        name = m.group(1) if m else tok
        fixes = []
        if name and defined_names:
            # Use Levenshtein distance for typo-aware suggestions
            close = _closest_names(name, defined_names, max_dist=3)
            if close:
                fixes.append(
                    "Possible typo — did you mean: "
                    + ", ".join(f"'{c}'" for c in close) + "?"
                )
        if name:
            fixes.append(
                f"Define '{name}' before this line, "
                f"e.g.: `{name} = <value>` or import it.")
            fixes.append(
                f"Check the spelling of '{name}' for typos.")
        return fixes or ["Define or import the name before using it."]

    # ── Invalid expression (covers missing comma, unexpected token) ────────
    if error_type == "INVALID_EXPRESSION":
        if "=>" in message or tok == ">":
            return [
                "Replace malformed operator `=>` with `>=`.",
                "Check for other mistyped comparison operators such as `=<` instead of `<=`.",
            ]
        if re.search(r"(?<![=!<>])=(?!=)", message) or "assignment" in msg:
            return [
                "If this is a comparison, replace `=` with `==`.",
                "Use plain `=` only for assignment statements, not inside conditions.",
            ]
        if "missing ','" in msg or "missing comma" in msg:
            return [
                f"Insert a ',' before '{tok}' to separate the arguments.",
                "Verify that every argument in the call/list is comma-separated.",
            ]
        if "unexpected token" in msg or "unexpected" in msg:
            return [
                f"Remove or replace the unexpected token '{tok}'.",
                "Check for missing operators, extra tokens, or keyword typos.",
            ]
        return [
            "Review the expression for missing operators, commas, or keywords.",
            f"The token '{tok}' is not valid at this position.",
        ]

    # ── Indentation ────────────────────────────────────────────────────────
    if error_type == "INDENTATION_ERROR":
        return [
            "Re-align this line to the correct indentation level (4 spaces per level).",
            "Ensure the line belongs to the right block — check the surrounding `def`/`if`/`for`.",
        ]

    if error_type == "INCONSISTENT_INDENTATION":
        return [
            "Convert all tabs to spaces (4 spaces per indent level).",
            "Use your editor's 'untabify' function or run: `expand -t 4 file.py`.",
        ]

    # ── Function / class definition problems ───────────────────────────────
    if error_type == "INVALID_FUNCTION_DEF":
        return [
            "Correct form: `def function_name(param1, param2):` — "
            "name, parentheses, and colon are all required.",
        ]

    if error_type == "INVALID_CLASS_DEF":
        return [
            "Correct form: `class ClassName:` or `class ClassName(BaseClass):`.",
        ]

    # ── Keyword misuse ─────────────────────────────────────────────────────
    if error_type == "KEYWORD_MISUSE":
        return [
            f"'{tok}' is a Python reserved keyword — choose a different name.",
            "Reserved words: if, for, while, def, class, return, import, …",
        ]

    # ── C / Java ───────────────────────────────────────────────────────────
    if error_type == "MISSING_SEMICOLON":
        return ["Add ';' at the end of the statement."]

    if error_type in ("INVALID_DECLARATION", "INVALID_SYNTAX"):
        return [
            "Review the statement against the language grammar.",
            "Check for missing type, name, modifiers, or closing semicolon.",
        ]

    if error_type == "INVALID_PREPROCESSOR":
        return [
            "Check the #include / #define syntax.",
            'Use angle brackets for system headers: #include <stdio.h>',
            'Use quotes for local headers: #include "myheader.h"',
        ]

    # ── End-of-file / too many errors ─────────────────────────────────────
    if error_type == "UnexpectedEOF":
        return [
            "Check for unclosed '(', '[', '{', or string literals.",
            "Every opening delimiter must have a matching closer.",
        ]

    if error_type == "MAX_ERRORS_EXCEEDED":
        return [
            "Fix the earliest structural syntax issue first: missing delimiter, bad operator, or indentation.",
            "The self-healer will keep trying follow-up repairs after the first fix to reduce cascaded errors.",
        ]

    # ── Control / Data Flow / Pattern analysis ─────────────────────────────
    if error_type == "UNREACHABLE_CODE":
        return [
            "Remove or restructure the code after the 'return'/'break'/'continue'.",
            "If the code is intentional, move it before the exit statement.",
        ]
    if error_type == "MISSING_RETURN":
        return [
            "Add a 'return' statement that covers all code paths.",
            "If the function intentionally returns None on some paths, "
            "add 'return None' explicitly for clarity.",
        ]
    if error_type == "BREAK_OUTSIDE_LOOP":
        return ["Move the 'break' statement inside a 'for' or 'while' loop."]
    if error_type == "CONTINUE_OUTSIDE_LOOP":
        return ["Move the 'continue' statement inside a 'for' or 'while' loop."]
    if error_type == "INFINITE_LOOP":
        return [
            "Add a 'break' statement inside the loop body to provide a way out.",
            "Or change the loop condition so it eventually becomes False.",
        ]
    if error_type == "UNUSED_VARIABLE":
        return [
            f"Remove the assignment to '{tok}' if it is not needed.",
            f"Or use it later in the code; perhaps a typo caused it to be read "
            f"under a different name.",
            "Use '_' or a name starting with '_' to signal intentional discard.",
        ]
    if error_type == "REDUNDANT_ASSIGNMENT":
        return [
            f"Remove the earlier assignment to '{tok}' since it is overwritten "
            f"before being read.",
            "Or read the value between the two assignments if that was your intent.",
        ]
    if error_type == "MUTABLE_DEFAULT_ARG":
        return [
            f"Change the default to None: `def f({tok}=None):` "
            f"then inside the function: `if {tok} is None: {tok} = []`",
        ]
    if error_type == "BARE_EXCEPT":
        return [
            "Replace bare 'except:' with 'except Exception as e:' "
            "to catch only non-system exceptions.",
            "Or specify the exact exception type, e.g. 'except ValueError:'.",
        ]
    if error_type == "EMPTY_EXCEPT":
        return [
            "Add error handling inside the except block: at minimum log the error.",
            "If you intentionally suppress it, add a comment explaining why.",
        ]
    if error_type == "IS_LITERAL_COMPARE":
        return [
            f"Replace 'is' with '==' for value comparison: `x == {tok}`",
        ]
    if error_type == "SINGLETON_COMPARE":
        return [
            f"Replace '==' with 'is': `x is {tok}` (or 'is not' for !=).",
        ]
    if error_type == "BUILTIN_SHADOW":
        return [
            f"Rename the variable '{tok}' to avoid hiding the built-in.",
            f"For example: '{tok}_list', 'my_{tok}', or any non-conflicting name.",
        ]
    if error_type == "UNUSED_IMPORT":
        return [
            f"Remove the unused import: 'import {tok}' (or the 'from … import' line).",
            "Or use the imported name somewhere in your code.",
        ]

    # ── Generic fallback ───────────────────────────────────────────────────
    return [
        "Review the flagged line and surrounding context for syntax mistakes.",
        "Check the previous line for an unclosed expression or missing token.",
    ]





# ═══════════════════════════════════════════════════════════════════════════
# PYTHON ANALYSIS  (rule-based classification; optional ML severity)
# ═══════════════════════════════════════════════════════════════════════════

def _try_ml_severity(feature_list, errors) -> list[float] | None:
    """Try to get per-error severity scores from the ML regressor.
    Returns None if models are unavailable."""
    try:
        import pickle, os as _os
        model_path = _os.path.join("ml", "model_severity.pkl")
        if not _os.path.exists(model_path):
            return None
        import sys as _sys
        import ml.train_classifier as _tc
        _sys.modules.setdefault("__main__", _sys.modules[__name__])
        _fake = _sys.modules.get("__main__")
        for _attr in ("_TextExtractor", "_NumericExtractor"):
            if not hasattr(_fake, _attr):
                setattr(_fake, _attr, getattr(_tc, _attr))
        import numpy as np
        with open(model_path, "rb") as f:
            reg = pickle.load(f)
        scores = np.clip(reg.predict(feature_list), 0, 10).tolist()
        return scores
    except Exception:
        return None


def analyse_python(source: str, filepath: str = "<input>",
                   no_heal: bool = False,
                   record_profile: bool = True) -> None:
    """Parse Python source, classify errors with rule-based logic, display.
    Also runs IR-based control flow, data flow, and pattern analyses."""
    from lexers import tokenize_python
    from parsers import parse_python
    try:
        from ml.ast_feature_extractor import ASTFeatureExtractor
    except Exception:
        ASTFeatureExtractor = None

    parse_failed = False
    total_started = time.perf_counter()
    parse_started = time.perf_counter()
    ir_program = None
    analysis_diags = []
    try:
        tokens = tokenize_python(source)
        ast_tree, errors = parse_python(tokens)
    except Exception as exc:
        parse_failed = True
        tokens = []
        ast_tree = None
        errors = _parse_errors(source, "python")
        print(f"  [INTERNAL ERROR] Tokenizer/parser raised: {exc}")
    parse_time_ms = (time.perf_counter() - parse_started) * 1000.0

    # ── IR Build + Multi-pass Analysis ────────────────────────────────────
    ir_build_time_ms = 0.0
    analysis_pass_ms = 0.0
    try:
        from ir import build_ir
        from analysis import run_all_analyses
        from syntax_tree import ast_nodes as _ast
        ir_started = time.perf_counter()
        ir_program = build_ir(ast_tree)
        ir_build_time_ms = (time.perf_counter() - ir_started) * 1000.0
        analysis_started = time.perf_counter()
        analysis_diags = run_all_analyses(ir_program, ast_tree, source)
        analysis_pass_ms = (time.perf_counter() - analysis_started) * 1000.0
        # Convert analysis diagnostics to ErrorNode-compatible objects
        for d in analysis_diags:
            err = _ast.ErrorNode(
                error_type=d.error_type,
                message=d.message,
                token=getattr(d, 'token', None),
                line=d.line,
                column=getattr(d, 'column', 0),
            )
            errors.append(err)
        # Re-sort merged list
        errors.sort(key=lambda e: (e.line, e.column))
    except Exception:
        pass  # IR analysis is additive; never block display of syntax errors

    src_lines = source.splitlines()
    _print_header(filepath, "Python", len(errors))
    security_report = None
    try:
        from analysis.security_vulnerability import build_security_report
        security_report = build_security_report(ast_tree)
    except Exception:
        security_report = None

    def _emit_perf_report() -> None:
        try:
            from analysis.performance_energy import build_reports
            report_data = build_reports(
                source=source,
                language="python",
                filepath=filepath,
                ast_tree=ast_tree,
                ir_program=ir_program,
                errors=errors,
                timing_breakdown={
                    "parse_time_ms": parse_time_ms,
                    "ir_build_time_ms": ir_build_time_ms,
                    "analysis_pass_ms": analysis_pass_ms,
                    "total_analysis_ms": (time.perf_counter() - total_started) * 1000.0,
                },
                persist=record_profile,
            )
            _print_performance_energy_sections(report_data)
        except Exception:
            pass

    if not errors:
        print()
        print(f"  {_TICK}  No issues detected. Your code looks clean!")
        print()
        print(BORDER)
        if not no_heal:
            heal_and_display(source, [], language="python",
                             defined_names=set())
        if security_report is not None:
            _print_security_report(security_report)
        _emit_perf_report()
        return

    # Collect defined names from the parser's module-level cache
    # (populated by parse_python after every parse run)
    try:
        from parsers.python_parser import _last_defined_names, _last_used_cols
        defined_names: set[str] = set(_last_defined_names)
        used_cols: dict[str, int] = dict(_last_used_cols)
    except Exception:
        defined_names = set()
        used_cols = {}
    # Patch in column numbers for UNDEFINED_NAME errors that have column 0
    for e in errors:
        if e.error_type == "UNDEFINED_NAME" and e.column == 0 and e.token:
            e.column = used_cols.get(e.token, 0)

    # Optional: get ML severity scores
    ml_scores: list[float] | None = None
    try:
        if parse_failed or ASTFeatureExtractor is None or ast_tree is None:
            raise ImportError("ASTFeatureExtractor not available")
        extractor    = ASTFeatureExtractor(tokens, ast_tree)
        feature_list = extractor.extract(errors)
        ml_scores    = _try_ml_severity(feature_list, errors)
    except Exception:
        pass

    # ── Annotated source view ─────────────────────────────────────────────
    by_line: dict = defaultdict(list)
    for e in errors:
        by_line[e.line].append(e)

    print()
    print(_section_title("Annotated Source"))
    print(f"  {_BOX_VT}")
    w = len(str(len(src_lines)))
    for i, code_line in enumerate(src_lines, start=1):
        prefix = f"  {_BOX_VT}  {str(i).rjust(w)} {_BOX_VT} "
        print(f"{prefix}{code_line}")
        if i in by_line:
            for e in by_line[i]:
                py_class, _, _, _ = classify_error(e.error_type)
                sev = _diagnostic_kind(e.error_type, py_class)
                # columns are 1-based from the lexer; convert to 0-based offset
                col    = max(e.column - 1, 0) if e.column else 0
                pad    = len(prefix) + col
                print(" " * pad + "^")
                indent = " " * (len(prefix) + 1)
                print(f"{indent}{_ARROW} [{sev}] {e.message}")
    print(f"  {_BOX_VT}")
    print(f"  {_BOX_BL}{HALF}")

    # ── Per-error detailed explanations ───────────────────────────────────
    print()
    print("  Detailed Error Explanations")
    print(THIN)

    for idx, e in enumerate(errors, 1):
        line_text = src_lines[e.line - 1] if 0 < e.line <= len(src_lines) else ""
        # columns are 1-based; convert to 0-based for caret positioning
        col     = max(e.column - 1, 0) if e.column else 0
        pointer = " " * col + "^"
        col_display = e.column if e.column else "(unknown)"

        py_class, score, title, explanation = classify_error(e.error_type)
        sev = _diagnostic_kind(e.error_type, py_class)
        fixes = generate_fixes(e.error_type, e.message, e.token, defined_names)

        print()
        print(f"  Issue #{idx}  --  Line {e.line}, Column {col_display}")
        print(f"  {HALF}")
        print(f"  Source code  :  {line_text}")
        if line_text:
            print(f"                  {pointer}")
        print(f"  Category     :  {sev}")
        print(f"  Rule class   :  {py_class}")
        print(f"  Rule type    :  {e.error_type}")
        print(f"  Message      :  {e.message}")
        print()
        print(f"  Severity     :  {score} / 10")
        print(f"  Title        :  {title}")
        print("  Explanation  :")
        print(_wrap(explanation))
        print()
        print("  How to fix   :")
        for i, fix in enumerate(fixes, 1):
            print(f"    #{i}  {fix}")
        if idx < len(errors):
            print()
            print(f"  {THIN}")

    print()
    print(BORDER)
    if not no_heal and errors:
        heal_and_display(source, errors, language="python",
                         defined_names=defined_names)
    if security_report is not None:
        _print_security_report(security_report)
    _emit_perf_report()
    print()


# ── C / Java analysis (parser + rule-based suggestions) ───────────────────────

def analyse_parser_only(source: str, filepath: str, language: str,
                        no_heal: bool = False,
                        record_profile: bool = True) -> None:
    """Run parser-based analysis for C, Java (or Python fallback)."""
    from lexers import tokenize_c, tokenize_java, tokenize_python
    from parsers import parse_c, parse_java, parse_python

    tokenizers = {"c": tokenize_c, "java": tokenize_java, "python": tokenize_python}
    parsers    = {"c": parse_c,    "java": parse_java,    "python": parse_python}

    lang_label = {"c": "C", "java": "Java", "python": "Python (Parser)"}[language]

    total_started = time.perf_counter()
    parse_started = time.perf_counter()
    ir_program = None

    try:
        tokens           = tokenizers[language](source)
        ast_tree, errors = parsers[language](tokens)
    except Exception as exc:
        errors = _parse_errors(source, language)
        print(f"  [INTERNAL ERROR] Parser raised: {exc}")
        tokens = []
        ast_tree = None
    parse_time_ms = (time.perf_counter() - parse_started) * 1000.0

    src_lines = source.splitlines()

    # Deduplicate errors: keep only the first occurrence of each (line, message) pair
    seen: set = set()
    unique_errors = []
    for e in errors:
        key = (e.line, e.message)
        if key not in seen:
            seen.add(key)
            unique_errors.append(e)
    errors = unique_errors

    _print_header(filepath, lang_label, len(errors))

    def _emit_perf_report() -> None:
        try:
            from analysis.performance_energy import build_reports
            report_data = build_reports(
                source=source,
                language=language,
                filepath=filepath,
                ast_tree=ast_tree,
                ir_program=ir_program,
                errors=errors,
                timing_breakdown={
                    "parse_time_ms": parse_time_ms,
                    "ir_build_time_ms": 0.0,
                    "analysis_pass_ms": 0.0,
                    "total_analysis_ms": (time.perf_counter() - total_started) * 1000.0,
                },
                persist=record_profile,
            )
            _print_performance_energy_sections(report_data)
        except Exception:
            pass

    if not errors:
        print()
        print(f"  {_TICK}  No issues detected. Your code looks clean!")
        print()
        print(BORDER)
        if not no_heal:
            heal_and_display(source, [], language=language)
        _emit_perf_report()
        return

    # ── Annotated source ──────────────────────────────────────────────────
    from collections import defaultdict
    by_line: dict = defaultdict(list)
    for e in errors:
        by_line[e.line].append(e)

    _print_annotated_source_plain(src_lines, by_line)

    # ── Per-error detail ──────────────────────────────────────────────────
    print()
    print("  Detailed Error Explanations")
    print(THIN)

    for idx, e in enumerate(errors, 1):
        line_text = src_lines[e.line - 1] if 0 < e.line <= len(src_lines) else ""
        col       = max(e.column - 1, 0) if e.column else 0
        pointer   = " " * col + "^"
        col_display = e.column if e.column else "(unknown)"

        py_class, score, title, explanation = classify_error(e.error_type)
        sev = _diagnostic_kind(e.error_type, py_class)
        fixes = generate_fixes(e.error_type, e.message, e.token, set())

        print()
        print(f"  Issue #{idx}  --  Line {e.line}, Column {col_display}")
        print(f"  {HALF}")
        print(f"  Source code  :  {line_text}")
        if line_text:
            print(f"                  {pointer}")
        print(f"  Category     :  {sev}")
        print(f"  Rule class   :  {py_class}")
        print(f"  Title        :  {title}")
        print(f"  Message      :  {e.message}")
        print()
        print(f"  Severity     :  {score} / 10")
        print("  Explanation  :")
        print(_wrap(explanation))
        print()
        print("  How to fix:")
        for i, fix in enumerate(fixes, 1):
            print(f"    #{i}  {fix}")

        if idx < len(errors):
            print()
            print(f"  {THIN}")

    print()
    print(BORDER)
    if not no_heal and errors:
        heal_and_display(source, errors, language=language)
    _emit_perf_report()
    print()


# ── Shared display helpers ────────────────────────────────────────────────────

def _print_header(filepath: str, lang_label: str, n_errors: int) -> None:
    status = f"{_CROSS}  ISSUES FOUND" if n_errors else f"{_TICK}  CLEAN"
    print()
    print(BORDER)
    print("  Syntax Error Analyzer")
    print(BORDER)
    print(f"  File     : {filepath}")
    print(f"  Language : {lang_label}")
    print(f"  Status   : {status}  ({n_errors} issue(s))")
    print(BORDER)


def _print_annotated_source(src_lines: list, by_line: dict) -> None:
    print()
    print(_section_title("Annotated Source"))
    print(f"  {_BOX_VT}")
    w = len(str(len(src_lines)))
    for i, code_line in enumerate(src_lines, start=1):
        prefix = f"  {_BOX_VT}  {str(i).rjust(w)} {_BOX_VT} "
        print(f"{prefix}{code_line}")
        if i in by_line:
            for d in by_line[i]:
                col = max(d.column - 1, 0)
                pad = len(prefix) + col
                print(" " * pad + "^")
                indent = " " * (len(prefix) + 1)
                print(f"{indent}{_ARROW} [{d.severity_label}] {d.error_message}")
    print(f"  {_BOX_VT}")
    print(f"  {_BOX_BL}" + HALF)

def _print_annotated_source_plain(src_lines: list, by_line: dict) -> None:
    """Annotated source for plain ErrorNode objects."""
    print()
    print(_section_title("Annotated Source"))
    print(f"  {_BOX_VT}")
    w = len(str(len(src_lines)))
    for i, code_line in enumerate(src_lines, start=1):
        prefix = f"  {_BOX_VT}  {str(i).rjust(w)} {_BOX_VT} "
        print(f"{prefix}{code_line}")
        if i in by_line:
            for e in by_line[i]:
                col   = max(e.column - 1, 0) if e.column else 0
                pad   = len(prefix) + col
                py_class, _, _, _ = classify_error(e.error_type)
                sev = _diagnostic_kind(e.error_type, py_class)
                print(" " * pad + "^")
                indent = " " * (len(prefix) + 1)
                print(f"{indent}{_ARROW} [{sev}] {e.message}")
    print(f"  {_BOX_VT}")
    print(f"  {_BOX_BL}" + HALF)


# ── Entry point ───────────────────────────────────────────────────────────────

_CONF_LABELS = [
    (0.9, "HIGH"),
    (0.7, "MEDIUM"),
    (0.0, "LOW"),
]


def _conf_label(confidence: float) -> str:
    for threshold, label in _CONF_LABELS:
        if confidence >= threshold:
            return label
    return "LOW"


def _parse_error_count(source: str, language: str) -> int | None:
    try:
        return len(_parse_errors(source, language))
    except Exception:
        return None


def _parse_errors(source: str, language: str) -> list:
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
    except Exception as exc:
        lines = source.splitlines() or [""]
        line_no = max(1, len(lines))
        column = len(lines[-1]) + 1 if lines else 1
        return [SimpleNamespace(
            error_type="MAX_ERRORS_EXCEEDED",
            message=f"Parser bailout: {exc}",
            line=line_no,
            column=column,
            token=None,
        )]


def _dedupe_strings(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def _infer_undefined_name(action) -> str:
    match = re.search(r"'([^']+)' is not defined", action.description or "")
    return match.group(1) if match else ""


def _suggested_line_variants(action) -> list[str]:
    variants: list[str] = []

    if action.repaired_line and action.repaired_line != action.original_line:
        variants.append(action.repaired_line)

    if action.error_type == "UNDEFINED_NAME" and action.suggestions:
        bad_name = _infer_undefined_name(action)
        if bad_name and action.original_line:
            pattern = r"\b" + re.escape(bad_name) + r"\b"
            for candidate in action.suggestions:
                replaced = re.sub(pattern, candidate, action.original_line, count=1)
                if replaced != action.original_line:
                    variants.append(replaced)
    elif action.suggestions:
        for candidate in action.suggestions:
            if candidate and candidate != action.original_line:
                variants.append(candidate)

    return _dedupe_strings(variants)


def _variant_confidence(action, variant: str, variant_index: int) -> float:
    if action.repaired_line and variant == action.repaired_line and action.confidence > 0:
        return action.confidence

    if action.error_type == "UNDEFINED_NAME" and action.suggestions:
        total = max(len(action.suggestions), 1)
        rank = min(variant_index, total - 1)
        return max(0.55, 0.85 - 0.10 * rank)

    if action.suggestions:
        total = max(len(action.suggestions), 1)
        rank = min(variant_index, total - 1)
        return max(0.35, action.confidence - 0.08 * rank)

    return max(action.confidence, 0.60)


def _build_fully_healed_candidates(base_source: str,
                                   actions: list,
                                   language: str,
                                   max_candidates: int = 6,
                                   max_combos: int = 48) -> list[dict]:
    option_sets: list[tuple[int, list[tuple[str, float]]]] = []

    for action in actions:
        if action.mode != "suggested":
            continue
        variants = _suggested_line_variants(action)
        if variants:
            scored_variants = [
                (variant, _variant_confidence(action, variant, idx))
                for idx, variant in enumerate(variants)
            ]
            option_sets.append((action.line, scored_variants))

    if not option_sets:
        return []

    combo_budget = 1
    for _, variants in option_sets:
        combo_budget *= len(variants)
        if combo_budget > max_combos:
            return []

    base_lines = base_source.splitlines()
    found: list[dict] = []
    seen: set[str] = set()

    def _search(idx: int, working_lines: list[str], scores: list[float]) -> None:
        if len(found) >= max_candidates:
            return
        if idx >= len(option_sets):
            candidate_source = "\n".join(working_lines)
            if base_source.endswith("\n"):
                candidate_source += "\n"
            if candidate_source in seen:
                return
            seen.add(candidate_source)
            if _parse_error_count(candidate_source, language) == 0:
                confidence = sum(scores) / len(scores) if scores else 1.0
                found.append({
                    "source": candidate_source,
                    "confidence": confidence,
                })
            return

        line_no, variants = option_sets[idx]
        if not (1 <= line_no <= len(working_lines)):
            _search(idx + 1, working_lines, scores)
            return

        original = working_lines[line_no - 1]
        for variant, confidence in variants:
            working_lines[line_no - 1] = variant
            _search(idx + 1, working_lines, scores + [confidence])
            if len(found) >= max_candidates:
                break
        working_lines[line_no - 1] = original

    _search(0, list(base_lines), [])
    found.sort(key=lambda item: item["confidence"], reverse=True)
    return found


def _print_source_block(title: str, source: str, language: str) -> None:
    print()
    print(f"  {title}")
    print(f"```{language}")
    text = source.rstrip("\n")
    if text:
        print(text)
    print("```")


def _print_performance_energy_sections(report_data: dict) -> None:
    print()
    print(BORDER)
    print("  Current Code Performance & Energy Report")
    print(BORDER)
    print(report_data["current"]["summary"])
    print()
    print("  Plot exports:")
    print(f"    - Energy vs LOC: {report_data['current']['exports']['energy_loc_svg']}")
    print(f"    - Hotspots: {report_data['current']['exports']['hotspots_svg']}")
    print()
    print(BORDER)
    print("  Cumulative Performance & Energy Report")
    print(BORDER)
    print(report_data["cumulative"]["summary"])
    print()
    print("  Plot exports:")
    print(f"    - Energy trend: {report_data['cumulative']['exports']['energy_trend_svg']}")
    print(f"    - LOC range totals: {report_data['cumulative']['exports']['loc_bucket_svg']}")
    print(f"  Persistent history: {report_data['history_path']}")
    print(BORDER)


def _print_security_report(security_report: dict) -> None:
    print()
    print(BORDER)
    print("  Security Vulnerability Analysis Report")
    print(BORDER)
    print(security_report["summary"])
    print(BORDER)


def _comment_prefix(language: str) -> str:
    return "#" if language == "python" else "//"


def _force_patch_first_error(source: str, error, language: str) -> str:
    from self_heal.source_patcher import lines_to_source, reindent_line, infer_indent_level

    lines = source.splitlines()
    if not lines:
        return source

    idx = max(min(error.line - 1, len(lines) - 1), 0)
    line = lines[idx]
    indent = len(line) - len(line.lstrip(" \t"))
    stripped = line.strip()
    err_type = getattr(error, "error_type", "")
    message = getattr(error, "message", "")

    if err_type in {"INDENTATION_ERROR", "INCONSISTENT_INDENTATION"}:
        target = infer_indent_level(lines, idx + 1)
        return lines_to_source(reindent_line(lines, idx + 1, target))

    if err_type == "MISSING_COLON" and language == "python" and stripped and not stripped.endswith(":"):
        lines[idx] = line.rstrip() + ":"
        return lines_to_source(lines)

    if err_type == "MISSING_SEMICOLON" and language in {"c", "java"} and stripped and not stripped.endswith(";"):
        lines[idx] = line.rstrip() + ";"
        return lines_to_source(lines)

    if err_type in {"MISSING_PAREN", "MISSING_BRACKET", "MISSING_BRACE"} and stripped:
        closer = {
            "MISSING_PAREN": ")",
            "MISSING_BRACKET": "]",
            "MISSING_BRACE": "}",
        }[err_type]
        lines[idx] = line.rstrip() + closer
        return lines_to_source(lines)

    if language == "python":
        if idx > 0 and lines[idx - 1].rstrip().endswith(":") and stripped:
            lines[idx] = " " * (len(lines[idx - 1]) - len(lines[idx - 1].lstrip()) + 4) + stripped
            return lines_to_source(lines)

        if err_type in {"UnexpectedEOF", "MAX_ERRORS_EXCEEDED"} and stripped.endswith(":") and idx == len(lines) - 1:
            lines.append(" " * (indent + 4) + "pass")
            return lines_to_source(lines)

    return lines_to_source(lines)


def _update_best_candidate(best_entry: dict | None,
                           source: str,
                           language: str,
                           confidence: float,
                           verified: bool) -> dict | None:
    remaining = _parse_error_count(source, language)
    if remaining is None:
        return best_entry
    candidate = {
        "source": source,
        "confidence": confidence,
        "verified": verified and remaining == 0,
        "remaining_errors": remaining,
    }
    if best_entry is None:
        return candidate
    if candidate["remaining_errors"] < best_entry.get("remaining_errors", 10**9):
        return candidate
    if candidate["remaining_errors"] == best_entry.get("remaining_errors", 10**9):
        if candidate["confidence"] > best_entry.get("confidence", 0.0):
            return candidate
    return best_entry


def _apply_suggested_variants(source: str,
                              actions: list,
                              language: str) -> dict | None:
    lines = source.splitlines()
    changed = False
    confidence_scores: list[float] = []

    for action in actions:
        if action.mode != "suggested":
            continue
        variants = _suggested_line_variants(action)
        if not variants:
            continue
        line_no = action.line
        if not (1 <= line_no <= len(lines)):
            continue
        variant = variants[0]
        if variant == lines[line_no - 1]:
            continue
        lines[line_no - 1] = variant
        confidence_scores.append(_variant_confidence(action, variant, 0))
        changed = True

    if not changed:
        return None

    candidate_source = "\n".join(lines)
    if source.endswith("\n"):
        candidate_source += "\n"
    remaining = _parse_error_count(candidate_source, language)
    if remaining is None:
        return None
    confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.45
    return {
        "source": candidate_source,
        "confidence": max(0.35, min(confidence, 0.95)),
        "verified": remaining == 0,
        "remaining_errors": remaining,
    }


def _force_total_heal_candidates(source: str,
                                 language: str,
                                 defined_names: set | None = None,
                                 max_candidates: int = 3) -> list[dict]:
    from self_heal import heal_source

    defined_names = defined_names or set()
    queue: list[tuple[str, float]] = [(source, 0.40)]
    seen: set[str] = {source}
    results: list[dict] = []
    best_entry = _update_best_candidate(None, source, language, 0.40, False)

    while queue and len(results) < max_candidates:
        current, base_confidence = queue.pop(0)

        for _ in range(24):
            errors = _parse_errors(current, language)
            best_entry = _update_best_candidate(best_entry, current, language, base_confidence, False)
            if not errors:
                results.append({
                    "source": current,
                    "confidence": min(max(base_confidence, 0.40), 0.99),
                    "verified": True,
                    "remaining_errors": 0,
                })
                break

            result = heal_source(current, errors, language=language, defined_names=defined_names)
            best_entry = _update_best_candidate(
                best_entry,
                result.healed_source,
                language,
                min(base_confidence + 0.05, 0.90),
                result.fully_healed,
            )
            suggestion_candidates = _build_fully_healed_candidates(
                result.healed_source, result.actions, language
            )
            for entry in suggestion_candidates:
                if _parse_error_count(entry["source"], language) == 0 and entry["source"] not in seen:
                    seen.add(entry["source"])
                    queue.append((entry["source"], max(base_confidence, entry["confidence"] * 0.9)))

            auto_suggested = _apply_suggested_variants(result.healed_source, result.actions, language)
            if auto_suggested is not None:
                best_entry = _update_best_candidate(
                    best_entry,
                    auto_suggested["source"],
                    language,
                    auto_suggested["confidence"],
                    auto_suggested["verified"],
                )
                if (
                    auto_suggested["source"] not in seen
                    and auto_suggested["remaining_errors"] < len(errors)
                ):
                    seen.add(auto_suggested["source"])
                    queue.append((auto_suggested["source"], auto_suggested["confidence"]))

            next_source = result.healed_source
            next_count = _parse_error_count(next_source, language)
            if next_source != current and next_count < len(errors):
                current = next_source
                base_confidence = min(base_confidence + 0.05, 0.85)
                continue

            forced = _force_patch_first_error(current, errors[0], language)
            forced_count = _parse_error_count(forced, language)
            if forced == current or forced_count >= len(errors):
                break
            current = forced
            base_confidence = max(0.20, base_confidence - 0.03)

        if len(results) >= max_candidates:
            break

    deduped: list[dict] = []
    seen_sources: set[str] = set()
    for entry in sorted(results, key=lambda item: item["confidence"], reverse=True):
        if entry["source"] not in seen_sources:
            seen_sources.add(entry["source"])
            deduped.append(entry)
    if deduped:
        return deduped[:max_candidates]
    return [best_entry] if best_entry is not None else []


def _print_healed_code_section(language: str,
                               result_source: str,
                               original_source: str,
                               after_count: int | None,
                               candidate_entries: list[dict],
                               verified_count: int) -> None:
    normalized_entries: list[dict] = []
    seen_sources: set[str] = set()
    for entry in candidate_entries:
        source = entry.get("source", "")
        if not source or source in seen_sources:
            continue
        seen_sources.add(source)
        remaining = entry.get("remaining_errors")
        if remaining is None:
            remaining = _parse_error_count(source, language)
        normalized_entries.append({
            **entry,
            "remaining_errors": remaining,
        })

    print()
    print(BORDER)
    print("  Healed Code")
    print(BORDER)

    if after_count == 0:
        _print_source_block("Final Fully Healed Code (0 parser errors)", result_source, language)
    else:
        remaining_label = after_count if after_count is not None else "unknown"
        _print_source_block(
            f"Current Healed Code ({remaining_label} parser errors remain)",
            result_source,
            language,
        )

        filtered_entries = [entry for entry in normalized_entries if entry["source"] != result_source]
        preferred_confidence = filtered_entries[0]["confidence"] if filtered_entries else None
        unique_confidences = {round(item["confidence"], 6) for item in filtered_entries}
        for idx, entry in enumerate(filtered_entries, 1):
            verified = entry.get("verified", True)
            remaining = entry.get("remaining_errors")
            title = (
                f"Fully Healed Candidate {idx} (0 parser errors)"
                if verified and remaining == 0 else
                f"Best-Effort Healed Candidate {idx} ({remaining} parser errors remain)"
            )
            if len(filtered_entries) == 1:
                title = (
                    "Final Fully Healed Code (0 parser errors)"
                    if verified and remaining == 0 else
                    f"Best-Effort Healed Code ({remaining} parser errors remain)"
                )
            if preferred_confidence is not None and len(unique_confidences) > 1:
                if abs(entry["confidence"] - preferred_confidence) < 1e-9:
                    title += f"  [Preferred, confidence {entry['confidence']:.0%}]"
                else:
                    title += f"  [Confidence {entry['confidence']:.0%}]"
            _print_source_block(title, entry["source"], language)

    print(BORDER)


def heal_and_display(source: str,
                     errors: list,
                     language: str = "python",
                     defined_names: set | None = None) -> None:
    """Run the existing self-healing engine and render its report."""
    fallback_candidates: list[dict] = []

    try:
        from self_heal import heal_source
    except Exception as exc:
        fallback_candidates = _force_total_heal_candidates(
            source,
            language,
            defined_names=defined_names,
        )
        print()
        print(BORDER)
        print(f"  {_WRENCH} Self-Healing Report")
        print(BORDER)
        print(f"  [SELF-HEAL] Unable to import self-healing engine: {exc}")
        print(BORDER)
        _print_healed_code_section(
            language=language,
            result_source=source,
            original_source=source,
            after_count=_parse_error_count(source, language),
            candidate_entries=fallback_candidates,
            verified_count=0,
        )
        return

    try:
        result = heal_source(
            source,
            errors,
            language=language,
            defined_names=defined_names or set(),
        )
    except Exception as exc:
        fallback_candidates = _force_total_heal_candidates(
            source,
            language,
            defined_names=defined_names,
        )
        print()
        print(BORDER)
        print(f"  {_WRENCH} Self-Healing Report")
        print(BORDER)
        print(f"  [SELF-HEAL] Internal error: {exc}")
        print(BORDER)
        _print_healed_code_section(
            language=language,
            result_source=source,
            original_source=source,
            after_count=_parse_error_count(source, language),
            candidate_entries=fallback_candidates,
            verified_count=0,
        )
        return

    before_count = _parse_error_count(source, language)
    after_count = _parse_error_count(result.healed_source, language)
    verified_count = result.repaired_count
    suggested_count = getattr(result, "suggested_count", 0)
    skipped_count = sum(1 for action in result.actions if action.mode == "skipped")
    fully_healed_candidates = _build_fully_healed_candidates(
        result.healed_source,
        result.actions,
        language,
    )
    if after_count == 0:
        fully_healed_candidates = [{
            "source": result.healed_source,
            "confidence": 1.0,
            "verified": True,
            "remaining_errors": 0,
        }]
    if not fully_healed_candidates:
        fully_healed_candidates = _force_total_heal_candidates(
            result.healed_source if result.healed_source else source,
            language,
            defined_names=defined_names,
        )

    if after_count == 0:
        status_badge = _TICK
    elif result.fully_healed:
        status_badge = _TICK
    elif fully_healed_candidates:
        status_badge = "~"
    elif verified_count:
        status_badge = "~"
    else:
        status_badge = _CROSS

    print()
    print(BORDER)
    print(f"  {_WRENCH} Self-Healing Report   "
          f"({verified_count} applied {_TICK}  |  "
          f"{suggested_count} suggested  |  "
          f"{skipped_count} skipped  |  "
          f"status {status_badge})")
    print(BORDER)

    if not result.actions:
        print("  No repair actions were generated.")
    else:
        for action in result.actions:
            conf_lbl = _conf_label(action.confidence)

            if action.mode == "applied":
                verified_label = f"{_TICK} Verified" if action.verified else f"{_CROSS} Unverified"
                print()
                print(f"  [APPLIED]  Line {action.line}  "
                      f"[{action.error_type}]  "
                      f"Confidence: {conf_lbl} ({action.confidence:.0%})  "
                      f"{verified_label}")
                if action.description:
                    print(f"  Action: {action.description}")
                continue

            if action.mode == "suggested":
                print()
                print(f"  [SUGGEST]  Line {action.line}  "
                      f"[{action.error_type}]  "
                      f"Confidence: {conf_lbl} ({action.confidence:.0%})")
                if action.description:
                    print(f"  Note: {action.description}")
                if action.suggestions:
                    print("  Candidates: " + ", ".join(f"'{s}'" for s in action.suggestions))
                continue

            print()
            print(f"  [SKIP]  Line {action.line}  [{action.error_type}]")
            if action.skip_reason:
                print(f"  Reason: {action.skip_reason}")

    print()
    if before_count is not None and after_count is not None:
        print(f"  Re-validation: parser issues {before_count} -> {after_count}")
    else:
        print("  Re-validation: unavailable")

    if after_count == 0:
        print(f"  {_TICK}  Fully healed: zero remaining parser errors.")
    elif result.fully_healed:
        print(f"  {_TICK}  Fully healed: zero remaining parser errors.")
    elif fully_healed_candidates:
        best_remaining = fully_healed_candidates[0].get("remaining_errors")
        if best_remaining == 0:
            print(f"  {_INFO}  Forced repair mode generated a parse-clean candidate program.")
        else:
            print(f"  {_INFO}  Forced repair mode generated a best-effort candidate with {best_remaining} remaining parser errors.")
    elif verified_count:
        print(f"  {_INFO}  Partial repair: {verified_count} repair(s) were applied, but parser errors remain.")
    elif suggested_count:
        print(f"  {_INFO}  No safe auto-apply completed; no fully healed candidate was found.")
    else:
        print(f"  {_CROSS}  No safe repairs could be applied automatically.")

    print(BORDER)
    _print_healed_code_section(
        language=language,
        result_source=result.healed_source,
        original_source=source,
        after_count=after_count,
        candidate_entries=fully_healed_candidates,
        verified_count=verified_count,
    )


def _parse_args() -> tuple[str | None, str | None, bool]:
    """
    Returns (source_filepath_or_None, forced_language_or_None, no_heal).
    Recognized flags:
      --lang python|c|java    Force language detection
      --no-heal               Disable self-healing pass
    """
    args     = sys.argv[1:]
    forced   = None
    files    = []
    no_heal  = False

    i = 0
    while i < len(args):
        if args[i] in ("--lang", "-l") and i + 1 < len(args):
            forced = args[i + 1].lower()
            i += 2
        elif args[i] == "--no-heal":
            no_heal = True
            i += 1
        else:
            files.append(args[i])
            i += 1

    filepath = files[0] if files else None
    return filepath, forced, no_heal


def main() -> None:
    filepath, forced_lang, no_heal = _parse_args()

    # ── Read source ───────────────────────────────────────────────────────
    if filepath:
        if not os.path.exists(filepath):
            print(f"Error: file not found -- '{filepath}'")
            sys.exit(1)
        with open(filepath, encoding="utf-8", errors="ignore") as fh:
            source = fh.read()
        language = forced_lang or _detect_language(filepath) or "python"
        label    = filepath
    elif not sys.stdin.isatty():
        # Piped input
        source   = sys.stdin.read()
        language = forced_lang or "python"
        label    = "<stdin>"
    else:
        # Interactive prompt
        print(BORDER)
        print("  ML-Powered Syntax Error Analyzer")
        print(BORDER)
        print()
        if forced_lang:
            print(f"  Language: {forced_lang.upper()}")
        else:
            print("  Language: Python (default). Use --lang c|java to change.")
        print()
        print("  Paste your code below.")
        print("  When finished press Enter -> Ctrl+Z -> Enter  (Windows)")
        print("                         or Enter -> Ctrl+D       (Linux/Mac)")
        print()
        try:
            source = sys.stdin.read()
        except (KeyboardInterrupt, EOFError):
            source = ""

        if not source.strip():
            print("  No code provided. Exiting.")
            sys.exit(0)

        language = forced_lang or "python"
        label    = "<input>"

    # ── Dispatch ──────────────────────────────────────────────────────────
    if language == "python":
        analyse_python(source, filepath=label, no_heal=no_heal)
    elif language in ("c", "java"):
        analyse_parser_only(source, filepath=label, language=language,
                            no_heal=no_heal)
    else:
        print(f"  Unsupported language '{language}'. Use python, c, or java.")
        sys.exit(1)


if __name__ == "__main__":
    main()
