"""
analyze_code.py — Syntax Error Analyzer
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
from collections import defaultdict
from typing import List, Tuple

# ── Add project root so all imports resolve ───────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── Force UTF-8 output on Windows so box-drawing chars render correctly ───────
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                                  errors="replace", line_buffering=True)

# ── Display helpers ───────────────────────────────────────────────────────────

BORDER = "═" * 70
THIN   = "─" * 70
HALF   = "─" * 50


def _wrap(text: str, width: int = 66, indent: str = "    ") -> str:
    return "\n".join(
        indent + line
        for line in textwrap.fill(text, width).split("\n")
    )


def _bar(confidence: float, width: int = 10) -> str:
    filled = int(round(confidence * width))
    return "█" * filled + "░" * (width - filled)


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
            "Fix the first reported error and re-run the analyzer.",
            "Cascading errors disappear once the root cause is resolved.",
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


def analyse_python(source: str, filepath: str = "<input>") -> None:
    """Parse Python source, classify errors with rule-based logic, display.
    Also runs IR-based control flow, data flow, and pattern analyses."""
    from lexers import tokenize_python
    from parsers import parse_python
    try:
        from ml.ast_feature_extractor import ASTFeatureExtractor
    except Exception:
        ASTFeatureExtractor = None

    try:
        tokens           = tokenize_python(source)
        ast_tree, errors = parse_python(tokens)
    except Exception as exc:
        print(f"  [INTERNAL ERROR] Tokenizer/parser raised: {exc}")
        return

    # ── IR Build + Multi-pass Analysis ────────────────────────────────────
    try:
        from ir import build_ir
        from analysis import run_all_analyses
        from syntax_tree import ast_nodes as _ast
        ir_program     = build_ir(ast_tree)
        analysis_diags = run_all_analyses(ir_program, ast_tree, source)
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

    if not errors:
        print()
        print("  ✓  No errors detected.  Your code looks clean!")
        print()
        print(BORDER)
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
        if ASTFeatureExtractor is None:
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
    print("  ┌─ Annotated Source")
    print("  │")
    w = len(str(len(src_lines)))
    for i, code_line in enumerate(src_lines, start=1):
        prefix = f"  │  {str(i).rjust(w)} │ "
        print(f"{prefix}{code_line}")
        if i in by_line:
            for e in by_line[i]:
                _, score, _, _ = classify_error(e.error_type)
                sev    = _severity_label(score)
                # columns are 1-based from the lexer; convert to 0-based offset
                col    = max(e.column - 1, 0) if e.column else 0
                pad    = len(prefix) + col
                print(" " * pad + "^")
                indent = " " * (len(prefix) + 1)
                print(f"{indent}└── [{sev}] {e.message}")
    print("  │")
    print("  └" + HALF)

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
        sev  = _severity_label(score)
        fixes = generate_fixes(e.error_type, e.message, e.token, defined_names)

        print()
        print(f"  Error #{idx}  ──  Line {e.line}, Column {col_display}")
        print(f"  {HALF}")
        print(f"  Source code  :  {line_text}")
        if line_text:
            print(f"                  {pointer}")
        print(f"  Error class  :  {py_class}")
        print(f"  Error type   :  {e.error_type}")
        print(f"  Message      :  {e.message}")
        print()
        print(f"  Severity     :  {score} / 10  [{sev}]  —  {title}")
        print()
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
    print()


# ── C / Java analysis (parser + rule-based suggestions) ───────────────────────

def analyse_parser_only(source: str, filepath: str, language: str) -> None:
    """Run parser-based analysis for C, Java (or Python fallback)."""
    from lexers import tokenize_c, tokenize_java, tokenize_python
    from parsers import parse_c, parse_java, parse_python

    tokenizers = {"c": tokenize_c, "java": tokenize_java, "python": tokenize_python}
    parsers    = {"c": parse_c,    "java": parse_java,    "python": parse_python}

    lang_label = {"c": "C", "java": "Java", "python": "Python (Parser)"}[language]

    try:
        tokens           = tokenizers[language](source)
        ast_tree, errors = parsers[language](tokens)
    except Exception as exc:
        print(f"  [INTERNAL ERROR] Parser raised: {exc}")
        return

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

    if not errors:
        print()
        print("  ✓  No syntax errors detected.  Your code looks clean!")
        print()
        print(BORDER)
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
        sev   = _severity_label(score)
        fixes = generate_fixes(e.error_type, e.message, e.token, set())

        print()
        print(f"  Error #{idx}  ──  Line {e.line}, Column {col_display}")
        print(f"  {HALF}")
        print(f"  Source code  :  {line_text}")
        if line_text:
            print(f"                  {pointer}")
        print(f"  Category     :  {py_class}")
        print(f"  Title        :  {title}")
        print(f"  Message      :  {e.message}")
        print(f"  Explanation  :  {explanation}")
        print()
        print(f"  Severity     :  {score} / 10  [{sev}]")
        print()
        print("  How to fix:")
        for i, fix in enumerate(fixes, 1):
            print(f"    #{i}  {fix}")

        if idx < len(errors):
            print()
            print(f"  {THIN}")

    print()
    print(BORDER)
    print()


# ── Shared display helpers ────────────────────────────────────────────────────

def _print_header(filepath: str, lang_label: str, n_errors: int) -> None:
    status = "✗  ERRORS FOUND" if n_errors else "✓  CLEAN"
    print()
    print(BORDER)
    print("  Syntax Error Analyzer")
    print(BORDER)
    print(f"  File     : {filepath}")
    print(f"  Language : {lang_label}")
    print(f"  Status   : {status}  ({n_errors} error(s))")
    print(BORDER)


def _print_annotated_source(src_lines: list, by_line: dict) -> None:
    """Annotated source for ML diagnostics (Diagnostic objects)."""
    print()
    print("  ┌─ Annotated Source ")
    print("  │")
    w = len(str(len(src_lines)))
    for i, code_line in enumerate(src_lines, start=1):
        prefix = f"  │  {str(i).rjust(w)} │ "
        print(f"{prefix}{code_line}")
        if i in by_line:
            for d in by_line[i]:
                col = max(d.column - 1, 0)
                pad = len(prefix) + col
                print(" " * pad + "^")
                indent = " " * (len(prefix) + 1)
                print(f"{indent}└── [{d.severity_label}] {d.error_message}")
    print("  │")
    print("  └" + HALF)


def _print_annotated_source_plain(src_lines: list, by_line: dict) -> None:
    """Annotated source for plain ErrorNode objects."""
    print()
    print("  ┌─ Annotated Source ")
    print("  │")
    w = len(str(len(src_lines)))
    for i, code_line in enumerate(src_lines, start=1):
        prefix = f"  │  {str(i).rjust(w)} │ "
        print(f"{prefix}{code_line}")
        if i in by_line:
            for e in by_line[i]:
                col   = max(e.column - 1, 0) if e.column else 0
                pad   = len(prefix) + col
                _, score, _, _ = classify_error(e.error_type)
                sev   = _severity_label(score)
                print(" " * pad + "^")
                indent = " " * (len(prefix) + 1)
                print(f"{indent}└── [{sev}] {e.message}")
    print("  │")
    print("  └" + HALF)


# ── Entry point ───────────────────────────────────────────────────────────────

def _parse_args() -> tuple[str | None, str | None]:
    """
    Returns (source_filepath_or_None, forced_language_or_None).
    Recognized flags: --lang python|c|java
    """
    args   = sys.argv[1:]
    forced = None
    files  = []

    i = 0
    while i < len(args):
        if args[i] in ("--lang", "-l") and i + 1 < len(args):
            forced = args[i + 1].lower()
            i += 2
        else:
            files.append(args[i])
            i += 1

    filepath = files[0] if files else None
    return filepath, forced


def main() -> None:
    filepath, forced_lang = _parse_args()

    # ── Read source ───────────────────────────────────────────────────────
    if filepath:
        if not os.path.exists(filepath):
            print(f"Error: file not found — '{filepath}'")
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
        print("  When finished press Enter → Ctrl+Z → Enter  (Windows)")
        print("                         or Enter → Ctrl+D       (Linux/Mac)")
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
        analyse_python(source, filepath=label)
    elif language in ("c", "java"):
        analyse_parser_only(source, filepath=label, language=language)
    else:
        print(f"  Unsupported language '{language}'. Use python, c, or java.")
        sys.exit(1)


if __name__ == "__main__":
    main()
