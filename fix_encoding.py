"""
fix_encoding.py
Fixes analyze_code.py which has CP1252-decoded UTF-16 box-drawing characters.

Mapping (CP1252 mis-decoding → correct Unicode):
  ΓòÉ  (\u0393\xf2\xc9) → ═  (\u2550)   DOUBLE HORIZONTAL
  ΓöÇ  (\u0393\xf6\xc7) → ─  (\u2500)   LIGHT HORIZONTAL
  ┌    → ┌  (may already be correct)
  │    → │
  └    → └
  └──  → └──

Also ensures:
  - File is written as UTF-8 with BOM suppressed
  - sys.stdout UTF-8 reconfiguration block uses reconfigure() (Python 3.7+)
  - ASCII fallback sentinel constants are added
"""

import re

TARGET = 'analyze_code.py'

with open(TARGET, encoding='utf-8', errors='replace') as f:
    text = f.read()

# ─── Step 1: Replace every corrupted rendering of box-drawing chars ──────────
# These are the exact sequences produced by reading a UTF-8 box-drawing
# character stream through a CP1252 / latin-1 decoder.

replacements = [
    # ═  U+2550  (used in BORDER = "═" * 70)
    # UTF-8: 0xE2 0x95 0x90  →  CP1252: Γ  ò  É  = \u0393 \xf2 \xc9
    ('\u0393\xf2\xc9', '\u2550'),  # ΓòÉ → ═
    # ─  U+2500
    # UTF-8: 0xE2 0x94 0x80  →  CP1252: Γ  ö  \x80 ... but \x80 = €
    # Actual observed: ΓöÇ  = \u0393 \xf6 \xc7
    ('\u0393\xf6\xc7', '\u2500'),  # ΓöÇ → ─
    # ┌  U+250C
    # UTF-8: 0xE2 0x94 0x8C  →  ΓöÄ  but often seen differently
    ('\u0393\xf6\u0160', '\u250c'),  # ┌
    # │  U+2502
    # UTF-8: 0xE2 0x94 0x82  →  Γö é  but seen as ΓöÂ
    ('\u0393\xf6\xc2', '\u2502'),   # │
    # └  U+2514
    # UTF-8: 0xE2 0x94 0x94  → ΓöÛ
    ('\u0393\xf6\xdb', '\u2514'),   # └
    # —  U+2014 em-dash
    ('\u0393\xc7\u0090', '\u2014'),
]

for bad, good in replacements:
    text = text.replace(bad, good)

# ─── Step 2: Replace remaining Γ-prefixed 3-char sequences heuristically ─────
# Any leftover \u0393 + two bytes that form a UTF-8 3-byte sequence prefix
# We scan for patterns and try to decode them as UTF-8.
def _fix_residual_mojibake(s: str) -> str:
    """
    Find and fix any remaining 3-char windows of the form
      \u0393 + char1 + char2
    where the original bytes [0xE2, byte1, byte2] form a valid UTF-8 codepoint.
    """
    result = []
    i = 0
    while i < len(s):
        if s[i] == '\u0393' and i + 2 < len(s):
            b1 = ord(s[i+1])
            b2 = ord(s[i+2])
            # Only try if b1 and b2 are in single-byte range (< 256)
            if b1 < 256 and b2 < 256:
                try:
                    decoded = bytes([0xE2, b1 & 0xFF, b2 & 0xFF]).decode('utf-8')
                    result.append(decoded)
                    i += 3
                    continue
                except (UnicodeDecodeError, ValueError):
                    pass
        result.append(s[i])
        i += 1
    return ''.join(result)

text = _fix_residual_mojibake(text)

# ─── Step 3: Fix the stdout reconfiguration block to use reconfigure() ────────
# Old approach: wrapping sys.stdout in TextIOWrapper (fragile)
# New approach: use reconfigure() which is safe on Python 3.7+
OLD_STDOUT_BLOCK = '''\
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                                  errors="replace", line_buffering=True)'''

NEW_STDOUT_BLOCK = '''\
# ── Ensure UTF-8 output on Windows; fall back to ASCII art if needed ──────────
def _configure_output() -> bool:
    """
    Attempt to switch stdout to UTF-8.
    Returns True if Unicode box-drawing is supported, False for ASCII fallback.
    """
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
            return True
        # Python < 3.7 fallback
        import io
        sys.stdout = io.TextIOWrapper(
            sys.stdout.buffer, encoding='utf-8',
            errors='replace', line_buffering=True)
        return True
    except Exception:
        return False  # plain ASCII will be used

_UNICODE_OK = _configure_output()'''

if OLD_STDOUT_BLOCK in text:
    text = text.replace(OLD_STDOUT_BLOCK, NEW_STDOUT_BLOCK)
    print("Replaced stdout block (old form).")
else:
    # May already be partially updated; insert before display helpers comment
    marker = '# ── Display helpers'
    if marker in text and '_configure_output' not in text:
        text = text.replace(
            marker,
            NEW_STDOUT_BLOCK + '\n\n' + marker
        )
        print("Inserted stdout block before display helpers.")
    else:
        print("Stdout block already updated or not found — skipped.")

# ─── Step 4: Replace BORDER/THIN/HALF with smart-fallback versions ────────────
OLD_CONSTANTS = '''\
BORDER = "\u2550" * 70
THIN   = "\u2500" * 70
HALF   = "\u2500" * 50'''

NEW_CONSTANTS = '''\
# Box-drawing constants: Unicode when supported, plain ASCII fallback
if _UNICODE_OK:
    BORDER = "\u2550" * 70          # ══════...
    THIN   = "\u2500" * 70          # ──────...
    HALF   = "\u2500" * 50          # ──────...
    _BOX_TL  = "\u250c"             # ┌
    _BOX_VT  = "\u2502"             # │
    _BOX_BL  = "\u2514"             # └
    _BOX_H   = "\u2500"             # ─
    _ARROW   = "\u2514\u2500\u2500" # └──
    _TICK    = "\u2713"             # ✓
    _CROSS   = "\u2717"             # ✗
    _INFO    = "\u2139"             # ℹ
    _WRENCH  = "\U0001f527"         # 🔧
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
    _WRENCH  = "[*]"'''

if '"\u2550" * 70' in text or '"\\u2550" * 70' in text:
    # Already has correct Unicode — just add fallback wrapper
    text = text.replace(
        'BORDER = "\u2550" * 70\nTHIN   = "\u2500" * 70\nHALF   = "\u2500" * 50',
        NEW_CONSTANTS
    )
    print("Replaced BORDER/THIN/HALF with fallback block.")
else:
    print("BORDER constants not found in expected form — manual check needed.")

# ─── Step 5: Replace inline box chars in functions with named constants ────────
# Patterns: "  ┌─ " → f"  {_BOX_TL}{_BOX_H} "  etc.
# We do targeted string replacements so we don't touch logic.

# Source annotation panels use hardcoded "  ┌─ Annotated Source "
text = text.replace(
    '    print("  \u250c\u2500 Annotated Source ")',
    '    print(f"  {_BOX_TL}{_BOX_H} Annotated Source ")'
)
text = text.replace(
    '    print("  \u250c\u2500 Annotated Source ")',
    '    print(f"  {_BOX_TL}{_BOX_H} Annotated Source ")'
)
text = text.replace('"  \u250c\u2500 Annotated Source "',
                    'f"  {_BOX_TL}{_BOX_H} Annotated Source "')
text = text.replace('"  \u2502"', 'f"  {_BOX_VT}"')
text = text.replace('"  \u2514" + HALF)', 'f"  {_BOX_BL}" + HALF)')
# Healed source panel
text = text.replace('"  \u250c\u2500 Healed Source  (auto-applied repairs only)"',
                    'f"  {_BOX_TL}{_BOX_H} Healed Source  (auto-applied repairs only)"')
# The "└──" error pointer
text = text.replace(
    'f"{indent}\u2514\u2500\u2500 [{',
    'f"{indent}{_ARROW} [{'
)
# heal_and_display badges
text = text.replace(
    '"  \u2713  All syntax errors resolved \u2014 healed source shown below."',
    'f"  {_TICK}  All syntax errors resolved -- healed source shown below."'
)
text = text.replace(
    '"\u2713  All syntax errors resolved \u2014 healed source shown below."',
    'f"  {_TICK}  All syntax errors resolved -- healed source shown below."'
)
text = text.replace('"\u2713 Verified"', 'f"{_TICK} Verified"')
text = text.replace('"\u2717 Unverified"', 'f"{_CROSS} Unverified"')
text = text.replace('"  \u2713  All syntax"', 'f"  {_TICK}  All syntax"')
text = text.replace('"  \u2717  No safe"', 'f"  {_CROSS}  No safe"')
text = text.replace('"\u2139  {suggested_count}', 'f"{_INFO}  {suggested_count}')
# Wrench emoji in Self-Healing header
text = text.replace('"  \U0001f527 Self-Healing Report', 'f"  {_WRENCH} Self-Healing Report')
# Clean source tick
text = text.replace('"  \u2713  No syntax errors detected.', 'f"  {_TICK}  No syntax errors detected.')
# Status symbols in header
text = text.replace('"\u2717  ERRORS FOUND"', 'f"{_CROSS}  ERRORS FOUND"')
text = text.replace('"\u2713  CLEAN"', 'f"{_TICK}  CLEAN"')

# ─── Step 6: Write corrected file ─────────────────────────────────────────────
with open(TARGET, 'w', encoding='utf-8') as f:
    f.write(text)

print(f"\nWrote {TARGET}  ({len(text)} chars, {text.count(chr(10))} lines)")

# ─── Step 7: Syntax check ─────────────────────────────────────────────────────
import py_compile
try:
    py_compile.compile(TARGET, doraise=True)
    print("Syntax check: OK")
except py_compile.PyCompileError as e:
    print(f"Syntax check: FAIL — {e}")
    import sys; sys.exit(1)
