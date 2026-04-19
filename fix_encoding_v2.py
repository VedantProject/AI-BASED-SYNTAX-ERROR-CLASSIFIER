"""
fix_encoding_v2.py
Complete fix for all mojibake in analyze_code.py and self_heal/healer.py.

The root cause: these files were saved as UTF-8 but at some point read/written
back through a CP1252/latin-1 codec, causing every multi-byte UTF-8 sequence to
be split into multiple single-byte CP1252 characters.

The mapping is systematic:
  UTF-8 byte [0xE2 0xNN 0xMM] →  read as CP1252: Γ (0xC3 = latin capital Γ?
  Actually in many cases the 0xE2 byte reads as â in latin-1, but in CP1252
  the sequences observed are different.

Empirical mapping from the file (read the literal escaped bytes):
  Γöî  = \\u0393 \\xf6 \\xce  = UTF-8 of ┌ (U+250C)?  No...

Let's be empirical: read the file as raw bytes and decode each 3-byte sequence.
"""

import os

TARGET_FILES = [
    'analyze_code.py',
    'self_heal/healer.py',
]

def fix_mojibake(text: str) -> str:
    """
    Scan the string character by character. Whenever we see a 3-char window
    [c0, c1, c2] where:
      - c0 is in the range CP1252 maps 0xC0-0xFF (i.e. Γ or similar high Latin)
      - c1, c2 are printable Latin chars
    try to decode [byte(c0), byte(c1), byte(c2)] as UTF-8.
    If it succeeds and produces a single non-ASCII codepoint, replace it.
    """
    # These are the exact observed mojibake sequences and their correct chars:
    EXPLICIT = {
        # From BORDER/THIN/HALF lines
        '\u0393\xf2\xc9':    '\u2550',  # ΓòÉ → ═
        '\u0393\xf6\xc7':    '\u2500',  # ΓöÇ → ─
        # Box-drawing chars in display functions
        '\u0393\xf6\xce':    '\u250c',  # Γöî → ┌  (U+250C: BOX DRAWINGS LIGHT DOWN AND RIGHT)
        '\u0393\xf6\u00e9':  '\u2502',  # Γöé → │  (U+2502: BOX DRAWINGS LIGHT VERTICAL)
        '\u0393\xf6\xf6':    '\u2514',  # Γöö → └  (U+2514: BOX DRAWINGS LIGHT UP AND RIGHT)
        # Tick / cross symbols
        '\u0393\xa3\xf9':    '\u2717',  # Γ£ù → ✗  (U+2717: BALLOT X)
        '\u0393\xa3\xf4':    '\u2713',  # Γ£ô → ✓  (U+2713: CHECK MARK)
        '\u0393\xa2\xb9':    '\u2139',  # ℹ
        # Em-dash
        '\u0393\xc7\x90':    '\u2014',  # — (EM DASH)
        # Arrow / └──
        # No 3-char form; the ── is already ─ repeated
    }

    for bad, good in EXPLICIT.items():
        text = text.replace(bad, good)

    # Heuristic residual pass: try every 3-char window where first char is
    # in the range [0xC0, 0xFF] to see if it decodes as a valid UTF-8 codepoint
    result = []
    i = 0
    while i < len(text):
        c0 = text[i]
        o0 = ord(c0)
        if 0xC0 <= o0 <= 0xFF and i + 2 < len(text):
            o1 = ord(text[i+1])
            o2 = ord(text[i+2])
            if o1 < 256 and o2 < 256:
                try:
                    decoded = bytes([o0, o1, o2]).decode('utf-8')
                    if len(decoded) == 1 and ord(decoded) > 0x7F:
                        result.append(decoded)
                        i += 3
                        continue
                except (UnicodeDecodeError, ValueError):
                    pass
        # Also try 4-byte emoji sequences (first byte 0xF0-0xF4)
        if 0xF0 <= o0 <= 0xF4 and i + 3 < len(text):
            o1 = ord(text[i+1]); o2 = ord(text[i+2]); o3 = ord(text[i+3])
            if o1 < 256 and o2 < 256 and o3 < 256:
                try:
                    decoded = bytes([o0, o1, o2, o3]).decode('utf-8')
                    if len(decoded) <= 2 and ord(decoded[0]) > 0x7F:
                        result.append(decoded)
                        i += 4
                        continue
                except (UnicodeDecodeError, ValueError):
                    pass
        result.append(c0)
        i += 1
    return ''.join(result)


def fix_file(path: str) -> None:
    with open(path, encoding='utf-8', errors='replace') as f:
        original = f.read()

    fixed = fix_mojibake(original)
    changed = sum(1 for a, b in zip(original, fixed) if a != b)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(fixed)

    print(f"  {path}: {changed} characters corrected")


print("Fixing mojibake in project files...")
for path in TARGET_FILES:
    if os.path.exists(path):
        fix_file(path)
    else:
        print(f"  SKIP {path} (not found)")

# Now specifically fix _print_header where the status uses raw chars
# Read and do targeted replacements for anything still remaining
print("\nApplying targeted fixes...")
for path in TARGET_FILES:
    if not os.path.exists(path):
        continue
    with open(path, encoding='utf-8') as f:
        text = f.read()

    before = text

    # Replace any remaining raw box chars with named constant references
    # in the display functions of analyze_code.py
    if path == 'analyze_code.py':
        # _print_header status line
        text = text.replace(
            'status = "\u2717  ERRORS FOUND" if n_errors else "\u2713  CLEAN"',
            'status = f"{_CROSS}  ERRORS FOUND" if n_errors else f"{_TICK}  CLEAN"'
        )
        # _print_annotated_source (ML)
        text = text.replace(
            '    print("  \u250c\u2500 Annotated Source ")\n    print("  \u2502")',
            '    print(f"  {_BOX_TL}{_BOX_H} Annotated Source ")\n    print(f"  {_BOX_VT}")'
        )
        text = text.replace(
            '        prefix = f"  \u2502  {str(i).rjust(w)} \u2502 "',
            '        prefix = f"  {_BOX_VT}  {str(i).rjust(w)} {_BOX_VT} "'
        )
        text = text.replace(
            '        print(f"{indent}\u2514\u2500\u2500 [{d.severity_label}] {d.error_message}")',
            '        print(f"{indent}{_ARROW} [{d.severity_label}] {d.error_message}")'
        )
        text = text.replace(
            '    print("  \u2502")\n    print("  \u2514" + HALF)\n\n\ndef _print_annotated_source_plain',
            '    print(f"  {_BOX_VT}")\n    print(f"  {_BOX_BL}" + HALF)\n\n\ndef _print_annotated_source_plain'
        )
        # _print_annotated_source_plain
        text = text.replace(
            '    print("  \u250c\u2500 Annotated Source ")\n    print("  \u2502")\n    w = len(str(len(src_lines)))\n    for i, code_line in enumerate(src_lines, start=1):\n        prefix = f"  \u2502  {str(i).rjust(w)} \u2502 "',
            '    print(f"  {_BOX_TL}{_BOX_H} Annotated Source ")\n    print(f"  {_BOX_VT}")\n    w = len(str(len(src_lines)))\n    for i, code_line in enumerate(src_lines, start=1):\n        prefix = f"  {_BOX_VT}  {str(i).rjust(w)} {_BOX_VT} "'
        )
        text = text.replace(
            '        print(f"{indent}\u2514\u2500\u2500 [{sev}] {e.message}")',
            '        print(f"{indent}{_ARROW} [{sev}] {e.message}")'
        )
        text = text.replace(
            '    print("  \u2502")\n    print("  \u2514" + HALF)\n\n\n# \u2500\u2500 Entry point',
            '    print(f"  {_BOX_VT}")\n    print(f"  {_BOX_BL}" + HALF)\n\n\n# \u2500\u2500 Entry point'
        )
        # Annotated source in heal_and_display
        text = text.replace(
            '        print("  \u250c\u2500 Healed Source  (auto-applied repairs only)")\n        print("  \u2502")',
            '        print(f"  {_BOX_TL}{_BOX_H} Healed Source  (auto-applied repairs only)")\n        print(f"  {_BOX_VT}")'
        )
        text = text.replace(
            '            prefix = f"  \u2502  {str(i).rjust(w)} \u2502 "',
            '            prefix = f"  {_BOX_VT}  {str(i).rjust(w)} {_BOX_VT} "'
        )
        text = text.replace(
            '        print("  \u2502")\n        print("  \u2514" + HALF)\n    print(BORDER)',
            '        print(f"  {_BOX_VT}")\n        print(f"  {_BOX_BL}" + HALF)\n    print(BORDER)'
        )
        # heal_and_display header badges
        text = text.replace(
            '"  \u2713  All syntax errors resolved \u2014 healed source shown below."',
            'f"  {_TICK}  All syntax errors resolved -- healed source shown below."'
        )
        text = text.replace(
            '"  \u2713  All syntax errors resolved — healed source shown below."',
            'f"  {_TICK}  All syntax errors resolved -- healed source shown below."'
        )
        text = text.replace('"\u2713 Verified"', 'f"{_TICK} Verified"')
        text = text.replace('"\u2717 Unverified"', 'f"{_CROSS} Unverified"')
        text = text.replace(
            '"  \u2717  No safe repairs could be determined automatically."',
            'f"  {_CROSS}  No safe repairs could be determined automatically."'
        )
        text = text.replace(
            'f"  \u2139  {suggested_count} suggestion(s)',
            'f"  {_INFO}  {suggested_count} suggestion(s)'
        )
        text = text.replace(
            'f"  \ud83d\udd27 Self-Healing Report',
            'f"  {_WRENCH} Self-Healing Report'
        )
        # Clean source message
        text = text.replace(
            '"  \u2713  No syntax errors detected.  Your code looks clean!"',
            'f"  {_TICK}  No syntax errors detected.  Your code looks clean!"'
        )

    if text != before:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"  {path}: targeted replacements applied")
    else:
        print(f"  {path}: no targeted replacements needed")

# Syntax check
import py_compile, sys
print("\nSyntax checks:")
all_ok = True
for path in TARGET_FILES:
    if not os.path.exists(path):
        continue
    try:
        py_compile.compile(path, doraise=True)
        print(f"  OK  {path}")
    except py_compile.PyCompileError as e:
        print(f"  FAIL  {path}: {e}")
        all_ok = False

sys.exit(0 if all_ok else 1)
