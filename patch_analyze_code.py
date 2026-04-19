"""
patch_analyze_code.py
An atomic patch script that applies ALL self-healing changes to analyze_code.py
in one safe operation.
"""
import re

SRC = 'analyze_code.py'

with open(SRC, encoding='utf-8') as f:
    text = f.read()

# ─────────────── 1. analyse_python signature ──────────────────────────────────
text = text.replace(
    'def analyse_python(source: str, filepath: str = "<input>") -> None:',
    'def analyse_python(source: str, filepath: str = "<input>",\n'
    '                   no_heal: bool = False) -> None:'
)

# ─────────────── 2. analyse_python — add healing call after final BORDER ──────
OLD_PY_END = '''    print()
    print(BORDER)
    print()


# ── C / Java analysis (parser + rule-based suggestions)'''
NEW_PY_END = '''    print()
    print(BORDER)

    # ── Self-Healing Pass ─────────────────────────────────────────────────────
    if not no_heal and errors:
        heal_and_display(source, errors, language="python",
                         defined_names=defined_names)
    print()


# ── C / Java analysis (parser + rule-based suggestions)'''
text = text.replace(OLD_PY_END, NEW_PY_END, 1)

# ─────────────── 3. analyse_parser_only signature ─────────────────────────────
text = text.replace(
    'def analyse_parser_only(source: str, filepath: str, language: str) -> None:',
    'def analyse_parser_only(source: str, filepath: str, language: str,\n'
    '                        no_heal: bool = False) -> None:'
)

# ─────────────── 4. analyse_parser_only — add healing call ──────────────────
# The function ends with:  print()\n    print(BORDER)\n    print()\n\n\n# ── Shared
OLD_C_END = '''    print()
    print(BORDER)
    print()


# ── Shared display helpers'''
NEW_C_END = '''    print()
    print(BORDER)

    # ── Self-Healing Pass ─────────────────────────────────────────────────────
    if not no_heal and errors:
        heal_and_display(source, errors, language=language)
    print()


# ── Shared display helpers'''
text = text.replace(OLD_C_END, NEW_C_END, 1)

# ─────────────── 5. Insert Self-Healing display section before Entry point ────
BEFORE_ENTRY = '# ── Entry point ─────────────────────────────────────────────────────────────'
HEAL_SECTION = '''# ── Self-Healing display ──────────────────────────────────────────────────────

# Confidence-level labels
_CONF_LABELS = [
    (0.9,  "HIGH"),
    (0.7,  "MEDIUM"),
    (0.0,  "LOW"),
]


def _conf_label(c: float) -> str:
    for threshold, label in _CONF_LABELS:
        if c >= threshold:
            return label
    return "LOW"


def heal_and_display(source: str,
                     errors: list,
                     language: str = "python",
                     defined_names: set | None = None) -> None:
    """
    Run the self-healing engine and display a styled Self-Healing Report.
    Called after the normal error output block.

    Three rendered modes per action
    --------------------------------
    [APPLIED]  — patch was auto-applied and verified by re-parse
    [SUGGEST]  — patch NOT applied; shown as a safe recommendation
    [SKIP]     — no rule applicable, conflict, or warning-only diagnostic
    """
    try:
        from self_heal import heal_source
    except ImportError:
        return  # self_heal module not installed — skip silently

    try:
        result = heal_source(
            source,
            errors,
            language=language,
            defined_names=defined_names or set(),
        )
    except Exception as exc:
        print(f"  [SELF-HEAL] Internal error: {exc}")
        return

    attempted = [a for a in result.actions if not a.skipped]
    if not attempted:
        return  # nothing to show

    verified_count  = result.repaired_count
    suggested_count = getattr(result, 'suggested_count', 0)
    heal_badge      = "✓" if result.fully_healed else ("~" if verified_count else "!")

    print()
    print(BORDER)
    print(f"  🔧 Self-Healing Report   "
          f"({verified_count} applied ✓  |  "
          f"{suggested_count} suggested  "
          f"{heal_badge})")
    print(BORDER)

    for idx, action in enumerate(result.actions, 1):

        if action.mode == "skipped":
            if action.skip_reason:
                print(f"  #{idx:>2} [SKIP]  Line {action.line}  "
                      f"[{action.error_type}]")
                print(f"        Reason: {action.skip_reason}")
            continue

        conf_lbl = _conf_label(action.confidence)

        if action.mode == "suggested":
            print()
            print(f"  #{idx:>2} [SUGGEST]  Line {action.line}  "
                  f"[{action.error_type}]  "
                  f"Confidence: {conf_lbl} ({action.confidence:.0%})"
                  f"  — NOT auto-applied")
            print(f"  {HALF}")
            if action.original_line:
                print(f"       was:  {action.original_line.rstrip()}")
            if action.repaired_line and action.repaired_line != action.original_line:
                print(f"       fix:  {action.repaired_line.rstrip()}")
            if action.description:
                print(f"      Note:  {action.description}")
            if action.suggestions:
                print("      Candidates: "
                      + ", ".join(f"'{s}'" for s in action.suggestions))
            continue

        # APPLIED
        v_badge = "✓ Verified" if action.verified else "✗ Unverified"
        print()
        print(f"  #{idx:>2} [APPLIED]  Line {action.line}  "
              f"[{action.error_type}]  "
              f"Confidence: {conf_lbl} ({action.confidence:.0%})  {v_badge}")
        print(f"  {HALF}")
        print(f"  - {action.original_line.rstrip()}")
        print(f"  + {action.repaired_line.rstrip()}")
        print(f"  Action: {action.description}")

    print()
    if result.fully_healed:
        print("  ✓  All syntax errors resolved — healed source shown below.")
    elif verified_count:
        print(f"  ~  {verified_count} repair(s) applied and verified by re-parse.")
        if suggested_count:
            print(f"     Additionally, {suggested_count} suggestion(s) above require "
                  "manual review.")
        print("     Re-run the analyzer on the healed source to check remaining issues.")
    elif suggested_count:
        print(f"  ℹ  {suggested_count} suggestion(s) listed — no safe auto-repairs. "
              "Review and apply manually.")
    else:
        print("  ✗  No safe repairs could be determined automatically.")

    # Only show healed source when at least one repair was actually applied
    if verified_count > 0:
        print()
        print("  ┌─ Healed Source  (auto-applied repairs only)")
        print("  │")
        src_lines = result.healed_source.splitlines()
        w = len(str(len(src_lines)))
        for i, code_line in enumerate(src_lines, start=1):
            prefix = f"  │  {str(i).rjust(w)} │ "
            print(f"{prefix}{code_line}")
        print("  │")
        print("  └" + HALF)
    print(BORDER)


'''
text = text.replace(BEFORE_ENTRY, HEAL_SECTION + BEFORE_ENTRY, 1)

# ─────────────── 6. _parse_args — add no_heal ─────────────────────────────────
OLD_PARSE_ARGS = '''def _parse_args() -> tuple[str | None, str | None]:
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
    return filepath, forced'''

NEW_PARSE_ARGS = '''def _parse_args() -> tuple[str | None, str | None, bool]:
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
    return filepath, forced, no_heal'''

text = text.replace(OLD_PARSE_ARGS, NEW_PARSE_ARGS, 1)

# ─────────────── 7. main() — unpack no_heal ───────────────────────────────────
text = text.replace(
    '    filepath, forced_lang = _parse_args()',
    '    filepath, forced_lang, no_heal = _parse_args()'
)

# ─────────────── 8. main() dispatch — pass no_heal ────────────────────────────
text = text.replace(
    '        analyse_python(source, filepath=label)',
    '        analyse_python(source, filepath=label, no_heal=no_heal)'
)
text = text.replace(
    '        analyse_parser_only(source, filepath=label, language=language)',
    '        analyse_parser_only(source, filepath=label, language=language,\n'
    '                            no_heal=no_heal)'
)

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(text)

print("Patch applied successfully.")
print(f"File size: {len(text)} chars, {text.count(chr(10))} lines")

# Quick syntax check
import py_compile, sys
try:
    py_compile.compile(SRC, doraise=True)
    print("Syntax check: OK")
except py_compile.PyCompileError as e:
    print(f"Syntax check: FAIL — {e}")
    sys.exit(1)
