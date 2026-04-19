"""Get exact codepoints of ALL chars in the remaining sequences."""
import subprocess, os
env = dict(os.environ); env['PYTHONIOENCODING'] = 'utf-8'
code = """
text = open('analyze_code.py', encoding='utf-8').read()
for i, line in enumerate(text.splitlines(), 1):
    if '\\u0393' in line:
        # Print all codepoints in the line
        j = line.index('\\u0393')
        window = line[max(0,j-2):j+5]
        codes = [f'U+{ord(c):04X}' for c in window]
        print(f'L{i}: {codes}')
        print(f'     chars: {window!r}')
"""
r = subprocess.run(['python', '-c', code], capture_output=True, env=env)
print(r.stdout.decode('utf-8', errors='replace'))
