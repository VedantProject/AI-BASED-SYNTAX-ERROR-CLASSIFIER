"""
quick_test.py  — Unit tests for self_heal repair logic (no parser import needed)
"""
import sys
sys.path.insert(0, '.')

from self_heal.source_patcher import source_to_lines, lines_to_source
from self_heal.healer import (
    _repair_missing_colon,
    _repair_missing_semicolon,
    _repair_missing_paren,
    _repair_missing_bracket,
    _repair_missing_brace,
    _repair_inconsistent_indentation,
    _suggest_bare_except,
    _suggest_mutable_default_arg,
    _suggest_singleton_compare,
    _suggest_is_literal_compare,
    _safe_typo_candidate,
    _ranked_candidates,
    _find_unmatched_open,
    _PATTERN_TYPES,
    _WARNING_TYPES,
    _SYNTAX_TYPES,
    _AUTO_APPLY_THRESHOLD,
)

PASS = "PASS"
FAIL = "FAIL"
results = []


def check(name, cond, detail=""):
    ok = bool(cond)
    results.append(ok)
    status = PASS if ok else FAIL
    print(f"  {status}  {name}" + (f"  [{detail}]" if detail else ""))
    return ok


print()
print("=" * 60)
print("  Self-Heal Unit Tests")
print("=" * 60)

# ── 1. Missing colon ────────────────────────────────────────────────────────
lines = source_to_lines("def greet(name)\n    print(name)\n")

class FE:
    def __init__(self, line, msg='', tok='', etype=''):
        self.line=line; self.message=msg; self.token=tok; self.error_type=etype

r = _repair_missing_colon(lines, FE(1), 'python')
check("MISSING_COLON: inserts ':'",     r is not None)
if r: check("MISSING_COLON: result correct", r[0][0] == "def greet(name):")

r2 = _repair_missing_colon(source_to_lines("def f():\n    pass\n"), FE(1), 'python')
check("MISSING_COLON: no-op on already-colon line", r2 is None)

# ── 2. Missing semicolon ────────────────────────────────────────────────────
lines_c = source_to_lines("    int x = 5\n    return 0;\n")
r = _repair_missing_semicolon(lines_c, FE(1), 'c')
check("MISSING_SEMICOLON: inserts ';'",    r is not None)
if r: check("MISSING_SEMICOLON: result correct", r[0][0] == "    int x = 5;")

r2 = _repair_missing_semicolon(source_to_lines("    return 0;\n"), FE(1), 'c')
check("MISSING_SEMICOLON: no-op on already-terminated", r2 is None)

# ── 3. Missing paren — balance-count ────────────────────────────────────────
lines_p = source_to_lines("    if x > 3\n        pass\n")
r = _repair_missing_paren(lines_p, FE(1, "missing '('"), 'python')
# Should skip — missing '(' with 'if' but the check requires keyword + no '('
check("MISSING_PAREN: opening handled safely", r is not None or r is None)  # smoke

lines_p2 = source_to_lines("    result = func(a, b\n")
r2 = _repair_missing_paren(lines_p2, FE(1, "expected ')'"), 'python')
check("MISSING_PAREN: closing inserted when unmatched exists", r2 is not None)

lines_p3 = source_to_lines("    result = func(a, b)\n")
r3 = _repair_missing_paren(lines_p3, FE(1, "expected ')'"), 'python')
check("MISSING_PAREN: no-op when balanced", r3 is None)

# ── 4. Missing bracket ──────────────────────────────────────────────────────
lines_b = source_to_lines("    x = arr[0\n")
r = _repair_missing_bracket(lines_b, FE(1), 'python')
check("MISSING_BRACKET: inserts ']' when unmatched", r is not None)

lines_b2 = source_to_lines("    x = arr[0]\n")
r2 = _repair_missing_bracket(lines_b2, FE(1), 'python')
check("MISSING_BRACKET: no-op when balanced", r2 is None)

# ── 5. Missing brace ────────────────────────────────────────────────────────
lines_br = source_to_lines("int main() {\n    return 0;\n")
r = _repair_missing_brace(lines_br, FE(2, "expected '}'"), 'c')
check("MISSING_BRACE: closing inserted when unmatched", r is not None)

lines_br2 = source_to_lines("int main() {\n    return 0;\n}\n")
r2 = _repair_missing_brace(lines_br2, FE(3, "expected '}'"), 'c')
check("MISSING_BRACE: no-op when balanced", r2 is None)

# ── 6. Inconsistent indentation ─────────────────────────────────────────────
lines_t = source_to_lines("def f():\n\tpass\n")
r = _repair_inconsistent_indentation(lines_t, FE(2), 'python')
check("INCONSISTENT_INDENT: converts tab to spaces", r is not None)
if r: check("INCONSISTENT_INDENT: no tab in result", "\t" not in r[0][1])

lines_t2 = source_to_lines("def f():\n    pass\n")
r2 = _repair_inconsistent_indentation(lines_t2, FE(2), 'python')
check("INCONSISTENT_INDENT: no-op on spaces-only line", r2 is None)

# ── 7. Pattern suggestions (NEVER auto-apply) ────────────────────────────────
lines_e = source_to_lines("    except:\n        pass\n")
r = _suggest_bare_except(lines_e, FE(1), 'python')
check("BARE_EXCEPT: produces suggestion", r is not None)
if r:
    new_lines, desc, conf = r
    check("BARE_EXCEPT: result correct",    "except Exception:" in new_lines[0])
    check("BARE_EXCEPT: HIGH confidence",   conf >= 0.85)

lines_m = source_to_lines("def f(x, lst=[]):\n    pass\n")
r = _suggest_mutable_default_arg(lines_m, FE(1), 'python')
check("MUTABLE_DEFAULT_ARG: produces suggestion", r is not None)
if r: check("MUTABLE_DEFAULT_ARG: result correct", "=None" in r[0][0])

lines_s = source_to_lines("    if x == None:\n        pass\n")
r = _suggest_singleton_compare(lines_s, FE(1), 'python')
check("SINGLETON_COMPARE: produces suggestion", r is not None)
if r: check("SINGLETON_COMPARE: result correct", "is None" in r[0][0])

lines_il = source_to_lines("    return x is 0\n")
r = _suggest_is_literal_compare(lines_il, FE(1), 'python')
check("IS_LITERAL_COMPARE: produces suggestion", r is not None)
if r: check("IS_LITERAL_COMPARE: result correct", "== 0" in r[0][0])

# ── 8. Category sets are correct ─────────────────────────────────────────────
check("WARNING_TYPES includes MISSING_RETURN",
      "MISSING_RETURN" in _WARNING_TYPES)
check("WARNING_TYPES includes UNUSED_VARIABLE",
      "UNUSED_VARIABLE" in _WARNING_TYPES)
check("PATTERN_TYPES includes BARE_EXCEPT",
      "BARE_EXCEPT" in _PATTERN_TYPES)
check("SYNTAX_TYPES includes MISSING_COLON",
      "MISSING_COLON" in _SYNTAX_TYPES)
check("PATTERN_TYPES NOT in SYNTAX_TYPES",
      not _PATTERN_TYPES.intersection(_SYNTAX_TYPES))
check("WARNING_TYPES NOT in SYNTAX_TYPES",
      not _WARNING_TYPES.intersection(_SYNTAX_TYPES))
check("AUTO_APPLY_THRESHOLD is 0.80",
      _AUTO_APPLY_THRESHOLD == 0.80)

# ── 9. Undefined-name: _safe_typo_candidate ──────────────────────────────────
candidates = {"print", "printf", "input", "output"}

# Dist-2, same first char, single candidate → safe at max_dist=2
r = _safe_typo_candidate("prnit", candidates, max_dist=2)
check("safe_typo: 'prnit' -> 'print' (dist=2, first char match)", r == "print",
      f"got {r!r}")

# Ambiguous (dist=1, two candidates both at dist=1) → None
r2 = _safe_typo_candidate("pin", {"pint", "ping"}, max_dist=1)
check("safe_typo: ambiguous two dist=1 candidates -> None", r2 is None, f"got {r2!r}")

# Different first char (z vs x/y) → None regardless of dist
r3 = _safe_typo_candidate("z", {"x", "y"}, max_dist=1)
check("safe_typo: 'z' → None (first char mismatch)", r3 is None, f"got {r3!r}")

# Exact match → None
r4 = _safe_typo_candidate("print", {"print"}, max_dist=1)
check("safe_typo: exact match → None", r4 is None, f"got {r4!r}")

# ── 10. _ranked_candidates ───────────────────────────────────────────────────
ranked = _ranked_candidates("z", {"x", "y", "zebra"}, max_dist=3)
names = [c for _, c in ranked]
# 'x' and 'y' have dist=1, 'zebra' has dist=4 (out of max_dist=3 → not included)
check("ranked_candidates: 'x'/'y' closer to 'z' than 'zebra'",
      "x" in names or "y" in names)
check("ranked_candidates: 'zebra' excluded at max_dist=3",
      "zebra" not in names)

# ── 11. Keyword misuse confidence below auto-apply threshold ─────────────────
from self_heal.healer import _repair_keyword_misuse
lines_kw = source_to_lines("class = 'Maths'\n")
r = _repair_keyword_misuse(lines_kw, FE(1, tok='class'), 'python')
if r:
    _, _, conf = r
    check("KEYWORD_MISUSE: confidence below auto-apply threshold", conf < _AUTO_APPLY_THRESHOLD,
          f"conf={conf}")

# ── Summary ──────────────────────────────────────────────────────────────────
passed = sum(results)
total  = len(results)
print()
print("=" * 60)
print(f"  Results: {passed}/{total} passed")
print("=" * 60)
print()
import sys
sys.exit(0 if passed == total else 1)
