"""
test_self_heal.py
==================
Automated tests for the self-healing compiler mechanism.

Run with:
    python test_self_heal.py

Each test provides a deliberately broken snippet, runs the healer,
and asserts that the healed source has fewer errors than the original.
"""

from __future__ import annotations

import sys
import os
import io
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from self_heal import heal_source
from analyze_code import _force_total_heal_candidates, heal_and_display


# ── Helpers ───────────────────────────────────────────────────────────────────

def _parse_errors(source: str, language: str) -> list:
    """Return error list from the appropriate parser."""
    if language == "python":
        from lexers import tokenize_python
        from parsers import parse_python
        tokens = tokenize_python(source)
        _, errors = parse_python(tokens)
    elif language == "c":
        from lexers import tokenize_c
        from parsers import parse_c
        tokens = tokenize_c(source)
        _, errors = parse_c(tokens)
    elif language == "java":
        from lexers import tokenize_java
        from parsers import parse_java
        tokens = tokenize_java(source)
        _, errors = parse_java(tokens)
    else:
        errors = []
    return errors


PASS = "\033[92m✓ PASS\033[0m"
FAIL = "\033[91m✗ FAIL\033[0m"


def _run(name: str, source: str, language: str, expect_reduction: bool = True):
    errors = _parse_errors(source, language)
    before = len(errors)

    result = heal_source(source, errors, language=language)
    after_errors = _parse_errors(result.healed_source, language)
    after = len(after_errors)

    reduced = after < before
    ok = reduced == expect_reduction

    status = PASS if ok else FAIL
    attempted = len([a for a in result.actions if not a.skipped])
    verified  = result.repaired_count

    print(f"  {status}  {name}")
    print(f"         Errors: {before} → {after}  |  "
          f"Repairs attempted: {attempted}, verified: {verified}")
    if not ok:
        print(f"         [!] Expected reduction={expect_reduction}, got reduced={reduced}")
    return ok


# ══════════════════════════════════════════════════════════════════════════════
# Python Tests
# ══════════════════════════════════════════════════════════════════════════════

def test_python_missing_colon():
    source = """\
def greet(name)
    print("Hello", name)
"""
    return _run("Python: MISSING_COLON (def)", source, "python")


def test_python_missing_colon_if():
    source = """\
x = 5
if x > 3
    print("big")
"""
    return _run("Python: MISSING_COLON (if)", source, "python")


def test_python_missing_colon_while():
    source = """\
i = 0
while i < 10
    i += 1
"""
    return _run("Python: MISSING_COLON (while)", source, "python")


def test_python_bare_except():
    source = """\
def safe_divide(a, b):
    try:
        return a / b
    except:
        return 0
"""
    return _run("Python: BARE_EXCEPT", source, "python")


def test_python_mutable_default_arg():
    source = """\
def append_item(item, lst=[]):
    lst.append(item)
    return lst
"""
    return _run("Python: MUTABLE_DEFAULT_ARG", source, "python")


def test_python_singleton_compare_none():
    source = """\
def check(x):
    if x == None:
        return True
    return False
"""
    return _run("Python: SINGLETON_COMPARE (== None)", source, "python")


def test_python_is_literal():
    source = """\
def is_zero(x):
    return x is 0
"""
    return _run("Python: IS_LITERAL_COMPARE", source, "python")


def test_python_inconsistent_indentation():
    source = "def foo():\n\tpass\n"
    return _run("Python: INCONSISTENT_INDENTATION", source, "python")


def test_python_undefined_name_typo():
    """'prnit' is a typo for 'print' — not in defined_names so may not fix,
    but healer should at least not crash."""
    source = """\
name = "World"
prnit(name)
"""
    errors = _parse_errors(source, "python")
    # Add 'print' as a known defined name to trigger typo suggestion
    result = heal_source(source, errors, language="python",
                         defined_names={"print", "name"})
    # Just check no exception raised and result is valid
    ok = isinstance(result.healed_source, str)
    status = PASS if ok else FAIL
    print(f"  {status}  Python: UNDEFINED_NAME typo (smoke test)")
    return ok


# ══════════════════════════════════════════════════════════════════════════════
# C Tests
# ══════════════════════════════════════════════════════════════════════════════

def test_c_missing_semicolon():
    source = """\
#include <stdio.h>

int main() {
    int x = 5
    printf("%d\\n", x);
    return 0;
}
"""
    return _run("C: MISSING_SEMICOLON", source, "c")


def test_c_missing_closing_brace():
    source = """\
#include <stdio.h>

int main() {
    int x = 5;
    printf("%d\\n", x);
    return 0;
"""
    return _run("C: MISSING_BRACE (closing)", source, "c")


# ══════════════════════════════════════════════════════════════════════════════
# Java Tests
# ══════════════════════════════════════════════════════════════════════════════

def test_java_missing_semicolon():
    source = """\
public class Hello {
    public static void main(String[] args) {
        int x = 10
        System.out.println(x);
    }
}
"""
    return _run("Java: MISSING_SEMICOLON", source, "java")


# ══════════════════════════════════════════════════════════════════════════════
# No-error baseline (healer should produce no actions)
# ══════════════════════════════════════════════════════════════════════════════

def test_clean_python_no_actions():
    source = """\
def add(a, b):
    return a + b

result = add(1, 2)
print(result)
"""
    errors = _parse_errors(source, "python")
    result = heal_source(source, errors, language="python")
    ok = result.repaired_count == 0 and result.healed_source == source
    status = PASS if ok else FAIL
    print(f"  {status}  Python: Clean source → zero repairs")
    return ok


def test_no_fake_fully_healed_fallback():
    source = "class\n"
    candidates = _force_total_heal_candidates(source, "python")
    ok = bool(candidates) and "source" in candidates[0]
    status = PASS if ok else FAIL
    print(f"  {status}  Python: forced repair returns a best-effort candidate")
    return ok


def test_healed_code_section_always_printed():
    source = "class\n"
    errors = _parse_errors(source, "python")
    buf = io.StringIO()
    with redirect_stdout(buf):
        heal_and_display(source, errors, language="python")
    output = buf.getvalue()
    ok = "Healed Code" in output
    status = PASS if ok else FAIL
    print(f"  {status}  Python: Healed Code section always shown")
    return ok


def test_python_operator_assignment_in_condition():
    source = """\
if x = 2:
    print(x)
"""
    errors = _parse_errors(source, "python")
    result = heal_source(source, errors, language="python", defined_names={"x", "print"})
    ok = "if x == 2:" in result.healed_source
    status = PASS if ok else FAIL
    print(f"  {status}  Python: repair '=' to '==' in condition")
    return ok


def test_c_operator_arrow_to_gte():
    source = """\
int main() {
    int x = 1;
    if (x => 2) {
        return 0;
    }
}
"""
    errors = _parse_errors(source, "c")
    result = heal_source(source, errors, language="c")
    ok = "if (x >= 2)" in result.healed_source
    status = PASS if ok else FAIL
    print(f"  {status}  C: repair '=>' to '>='")
    return ok


def test_python_bailout_continues_healing():
    source = """\
if x = 2
    print(x
"""
    errors = _parse_errors(source, "python")
    result = heal_source(source, errors, language="python", defined_names={"x", "print"})
    ok = result.repaired_count >= 2
    status = PASS if ok else FAIL
    print(f"  {status}  Python: continue healing after initial cascade")
    return ok


# ══════════════════════════════════════════════════════════════════════════════
# Runner
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print()
    print("═" * 60)
    print("  Self-Healing Compiler — Test Suite")
    print("═" * 60)
    print()

    tests = [
        test_python_missing_colon,
        test_python_missing_colon_if,
        test_python_missing_colon_while,
        test_python_bare_except,
        test_python_mutable_default_arg,
        test_python_singleton_compare_none,
        test_python_is_literal,
        test_python_inconsistent_indentation,
        test_python_undefined_name_typo,
        test_c_missing_semicolon,
        test_c_missing_closing_brace,
        test_java_missing_semicolon,
        test_clean_python_no_actions,
        test_no_fake_fully_healed_fallback,
        test_healed_code_section_always_printed,
        test_python_operator_assignment_in_condition,
        test_c_operator_arrow_to_gte,
        test_python_bailout_continues_healing,
    ]

    results = []
    for t in tests:
        try:
            results.append(t())
        except Exception as exc:
            print(f"  \033[91m✗ EXCEPTION\033[0m  {t.__name__}: {exc}")
            results.append(False)

    passed = sum(results)
    total  = len(results)
    print()
    print("═" * 60)
    print(f"  Results: {passed}/{total} passed")
    print("═" * 60)
    print()

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
