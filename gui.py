"""
gui.py — ML-Powered Syntax Error Analyzer
==========================================
A professional dark-themed Tkinter GUI that drives the existing
analyse_python() / analyse_parser_only() functions from analyze_code.py.

Run:
    python gui.py
"""

from __future__ import annotations

import io
import os
import re
import subprocess
import sys
import tempfile
import textwrap
import threading
import time
import tkinter as tk
from tkinter import filedialog, font, messagebox, scrolledtext, ttk

# ── Make sure the project root is importable ────────────────────────────────
_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

# ── Colour palette (light theme) ────────────────────────────────────────────
C = {
    "bg":          "#ffffff",   # main background
    "bg2":         "#ffffff",   # headers / panels
    "bg3":         "#f8fafc",   # editor bg
    "surface":     "#dbe4ee",   # separator / subtle elements
    "accent":      "#2563eb",   # primary accent
    "accent2":     "#7c3aed",   # secondary accent
    "accent3":     "#15803d",   # green (clean)
    "error":       "#dc2626",   # red (errors)
    "warn":        "#d97706",   # orange (warnings)
    "info":        "#0891b2",   # cyan (info)
    "text":        "#0f172a",   # main text
    "text_dim":    "#64748b",   # dimmed text
    "lineno":      "#eef2f7",   # line number gutter bg
    "status_ok":   "#15803d",
    "status_err":  "#dc2626",
    "btn_bg":      "#2563eb",
    "btn_fg":      "#ffffff",
    "btn_hover":   "#1d4ed8",
    "btn2_bg":     "#e2e8f0",
    "btn2_fg":     "#0f172a",
    "btn2_hover":  "#cbd5e1",
    "tab_active":  "#ffffff",
    "tab_inactive":"#f8fafc",
}

# ── Syntax-highlight token patterns (Python) ────────────────────────────────
_PY_PATTERNS = [
    ("keyword",  r"\b(False|None|True|and|as|assert|async|await|break|class|"
                 r"continue|def|del|elif|else|except|finally|for|from|global|"
                 r"if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|"
                 r"try|while|with|yield)\b"),
    ("builtin",  r"\b(abs|all|any|bin|bool|bytearray|bytes|callable|chr|"
                 r"classmethod|compile|complex|delattr|dict|dir|divmod|"
                 r"enumerate|eval|exec|filter|float|format|frozenset|getattr|"
                 r"globals|hasattr|hash|help|hex|id|input|int|isinstance|"
                 r"issubclass|iter|len|list|locals|map|max|memoryview|min|"
                 r"next|object|oct|open|ord|pow|print|property|range|repr|"
                 r"reversed|round|set|setattr|slice|sorted|staticmethod|str|"
                 r"sum|super|tuple|type|vars|zip)\b"),
    ("string",   r'("""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"[^"\n]*"|\'[^\'\n]*\')'),
    ("comment",  r"#[^\n]*"),
    ("number",   r"\b(\d+\.?\d*([eE][+-]?\d+)?|0[xX][0-9a-fA-F]+)\b"),
    ("decorator",r"@\w+"),
    ("funcname", r"def\s+(\w+)"),
    ("classname",r"class\s+(\w+)"),
    ("operator", r"[=<>!&|^~%*/+\-]+"),
    ("paren",    r"[\(\)\[\]\{\}]"),
]

_PY_COLORS = {
    "keyword":   "#cba6f7",
    "builtin":   "#89dceb",
    "string":    "#a6e3a1",
    "comment":   "#6c7086",
    "number":    "#fab387",
    "decorator": "#f5c2e7",
    "funcname":  "#89b4fa",
    "classname": "#f9e2af",
    "operator":  "#89b4fa",
    "paren":     "#cba6f7",
}

# ── Sample code snippets ─────────────────────────────────────────────────────
_SAMPLES = {
    "python": '''\
def greet(name)
    message = f"Hello, {name}!"
    print(message

def calculate(x, y):
    result = x + z          # z is undefined
    if result > 10
        print("Big number")
    return result

greet("World"
calculate(5, 3)
''',
    "c": '''\
#include <stdio.h>

int factorial(int n) {
    if (n <= 1) {
        return 1
    }
    return n * factorial(n - 1);
}

int main() {
    int num = 5
    printf("Factorial of %d is %d\\n", num, factorial(num))
    return 0;
}
''',
    "java": '''\
public class Example {
    public static int add(int a, int b) {
        return a + b
    }

    public static void main(String[] args) {
        int result = add(5, 10)
        if (result > 10) {
            System.out.println("Greater");
        
    }
}
''',
}


# ════════════════════════════════════════════════════════════════════════════
# Utilities
# ════════════════════════════════════════════════════════════════════════════

class StdoutCapture(io.StringIO):
    """Redirect stdout/stderr to an internal buffer during analysis."""
    pass



def _render_ir_program_view(ir_program) -> list:
    """
    Render an already-built IR program into a list of (text, tag) chunks
    for display in the IR View tab.
    """
    lines = []

    def _add(text, tag=""):
        lines.append((text, tag))

    try:
        if ir_program is None:
            return lines

        all_cfgs = ir_program.all_cfgs()
        total_blocks  = sum(len(cfg.blocks) for _, cfg in all_cfgs)
        total_instrs  = sum(
            sum(len(b.instrs) for b in cfg.blocks.values())
            for _, cfg in all_cfgs
        )

        _add("═" * 68 + "\n", "ir_header")
        _add("  Intermediate Representation  (Three-Address Code + CFG)\n", "ir_header")
        _add("═" * 68 + "\n", "ir_header")
        _add(f"  Functions : {len(ir_program.functions)}"
             f"   │  Basic Blocks : {total_blocks}"
             f"   │  TAC Instructions : {total_instrs}\n\n", "ir_summary")

        for fn_name, cfg in all_cfgs:
            _add(f"┌─ {fn_name} ─{'─' * max(0, 60 - len(fn_name))}\n", "ir_block")
            _add(f"│  Blocks: {len(cfg.blocks)}"
                 f"   Entry: {cfg.entry}   Exit: {cfg.exit}\n", "ir_edge")
            _add("│\n", "ir_edge")

            # CFG edges summary
            _add("│  CFG Edges:\n", "ir_edge")
            for bid, block in cfg.blocks.items():
                if block.successors:
                    succs = ", ".join(block.successors)
                    _add(f"│    {bid:20s} → {succs}\n", "ir_edge")

            _add("│\n", "ir_edge")

            # TAC instructions per block
            for bid, block in cfg.blocks.items():
                if not block.instrs:
                    continue
                _add(f"│  [{bid}]\n", "ir_block")
                for instr in block.instrs:
                    # Colour by opcode
                    op_tag = "ir_op"
                    text = str(instr)
                    _add(f"│      {text}\n", op_tag)

            _add("└" + "─" * 67 + "\n\n", "ir_block")

    except Exception as exc:
        import traceback
        _add(f"[IR Build Error] {exc}\n", "ir_op")
        _add(traceback.format_exc(), "")

    return lines


def _build_ir_view(source: str) -> list:
    """
    Build the IR from source and return a list of (text, tag) chunks
    for display in the IR View tab.
    """
    try:
        from lexers import tokenize_python
        from parsers import parse_python
        from ir import build_ir

        tokens = tokenize_python(source)
        ast_tree, _ = parse_python(tokens)
        ir_program = build_ir(ast_tree)
        return _render_ir_program_view(ir_program)
    except Exception as exc:
        return [(f"[IR Build Error] {exc}\n", "ir_op")]


def run_analysis(source: str, language: str) -> str:
    """
    Run the appropriate analyzer and return its text output as a string.
    Works by temporarily redirecting sys.stdout.
    """
    buf = StdoutCapture()
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = buf
    sys.stderr = buf
    try:
        if language == "python":
            from analyze_code import analyse_python
            analyse_python(source, filepath="<editor>", record_profile=False)
        elif language in ("c", "java"):
            from analyze_code import analyse_parser_only
            analyse_parser_only(source, filepath="<editor>", language=language, record_profile=False)
        else:
            buf.write("Unsupported language.\n")
    except Exception as exc:
        import traceback
        buf.write(f"\n[GUI ERROR] {exc}\n")
        traceback.print_exc(file=buf)
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
    return buf.getvalue()


def count_errors(output: str) -> int:
    """Extract error count from the analyzer header line."""
    m = re.search(r"\((\d+)\s+error", output)
    return int(m.group(1)) if m else 0


def detect_input_calls(source: str) -> int:
    """
    Count how many times input() is called in the source code.
    Uses a simple regex; handles most common patterns.
    """
    # Match input() or input("...") — not inside comments
    lines = source.splitlines()
    count = 0
    for line in lines:
        code_part = line.split("#")[0]  # strip comments
        count += len(re.findall(r"\binput\s*\(", code_part))
    return count


def run_code(source: str, user_inputs: list[str], timeout: int = 15) -> tuple[str, str, int]:
    """
    Execute Python source code and return (stdout, stderr, returncode).
    user_inputs is joined with newlines and piped to stdin.
    """
    # Write source to a temp file so tracebacks show correct line numbers
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(source)
        tmp_path = tmp.name

    try:
        stdin_data = "\n".join(user_inputs) + "\n" if user_inputs else ""
        result = subprocess.run(
            [sys.executable, tmp_path],
            input=stdin_data,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", f"[Execution timed out after {timeout}s]", -1
    except Exception as exc:
        return "", f"[Execution error] {exc}", -1
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def build_ast(source: str, language: str):
    """
    Call the lexer + parser directly (without stdout redirect) and return
    the AST root node.  Returns None on any failure.
    """
    try:
        if language == "python":
            from lexers import tokenize_python
            from parsers import parse_python
            tokens = tokenize_python(source)
            ast_tree, _ = parse_python(tokens)
            return ast_tree
        elif language == "c":
            from lexers import tokenize_c
            from parsers import parse_c
            tokens = tokenize_c(source)
            ast_tree, _ = parse_c(tokens)
            return ast_tree
        elif language == "java":
            from lexers import tokenize_java
            from parsers import parse_java
            tokens = tokenize_java(source)
            ast_tree, _ = parse_java(tokens)
            return ast_tree
    except Exception:
        return None


def build_report_payload(source: str, language: str) -> dict:
    """
    Rebuild AST/IR artifacts for performance-energy reporting without touching
    parser or self-healing logic. Returns a payload compatible with
    analysis.performance_energy.build_reports().
    """
    payload = {
        "ast_root": None,
        "ir_program": None,
        "errors": [],
        "timing": {
            "parse_time_ms": 0.0,
            "ir_build_time_ms": 0.0,
            "analysis_pass_ms": 0.0,
            "total_analysis_ms": 0.0,
        },
    }

    started = time.perf_counter()
    parse_started = time.perf_counter()
    try:
        if language == "python":
            from lexers import tokenize_python
            from parsers import parse_python
            tokens = tokenize_python(source)
            ast_root, errors = parse_python(tokens)
        elif language == "c":
            from lexers import tokenize_c
            from parsers import parse_c
            tokens = tokenize_c(source)
            ast_root, errors = parse_c(tokens)
        elif language == "java":
            from lexers import tokenize_java
            from parsers import parse_java
            tokens = tokenize_java(source)
            ast_root, errors = parse_java(tokens)
        else:
            return payload
        payload["ast_root"] = ast_root
        payload["errors"] = list(errors or [])
    except Exception:
        return payload
    payload["timing"]["parse_time_ms"] = (time.perf_counter() - parse_started) * 1000.0

    if language == "python" and payload["ast_root"] is not None:
        try:
            from ir import build_ir
            from analysis import run_all_analyses
            from syntax_tree import ast_nodes as _ast

            ir_started = time.perf_counter()
            payload["ir_program"] = build_ir(payload["ast_root"])
            payload["timing"]["ir_build_time_ms"] = (time.perf_counter() - ir_started) * 1000.0

            analysis_started = time.perf_counter()
            analysis_diags = run_all_analyses(payload["ir_program"], payload["ast_root"], source)
            payload["timing"]["analysis_pass_ms"] = (time.perf_counter() - analysis_started) * 1000.0

            for diag in analysis_diags:
                payload["errors"].append(_ast.ErrorNode(
                    error_type=diag.error_type,
                    message=diag.message,
                    token=getattr(diag, "token", None),
                    line=diag.line,
                    column=getattr(diag, "column", 0),
                ))

            payload["errors"].sort(key=lambda e: (e.line, e.column))
        except Exception:
            pass

    payload["timing"]["total_analysis_ms"] = (time.perf_counter() - started) * 1000.0
    return payload


# ── Node-type → display colour tag ──────────────────────────────────────────
_AST_NODE_TAGS = {
    # structural
    "Program":       "ast_root",
    "Block":         "ast_block",
    # declarations
    "FunctionDecl":  "ast_func",
    "ClassDecl":     "ast_class",
    "Parameter":     "ast_param",
    "VariableDecl":  "ast_var",
    # statements
    "IfStmt":        "ast_ctrl",
    "WhileStmt":     "ast_ctrl",
    "ForStmt":       "ast_ctrl",
    "ReturnStmt":    "ast_kw",
    "BreakStmt":     "ast_kw",
    "ContinueStmt":  "ast_kw",
    "ImportStmt":    "ast_import",
    "ExpressionStmt":"ast_stmt",
    # expressions
    "BinaryOp":      "ast_op",
    "UnaryOp":       "ast_op",
    "AssignmentExpr":"ast_assign",
    "FunctionCall":  "ast_call",
    "Literal":       "ast_literal",
    "Identifier":    "ast_ident",
    "ArrayAccess":   "ast_op",
    "MemberAccess":  "ast_op",
    # errors
    "ErrorNode":     "ast_error",
}

# Colours for each AST tag
_AST_TAG_COLORS = {
    "ast_root":    ("#89b4fa", "bold"),       # blue
    "ast_block":   ("#7f849c", "normal"),      # dim
    "ast_func":    ("#cba6f7", "bold"),        # purple
    "ast_class":   ("#f9e2af", "bold"),        # yellow
    "ast_param":   ("#89dceb", "normal"),      # cyan
    "ast_var":     ("#cdd6f4", "normal"),      # text
    "ast_ctrl":    ("#fab387", "bold"),        # orange
    "ast_kw":      ("#fab387", "normal"),      # orange
    "ast_import":  ("#a6e3a1", "normal"),      # green
    "ast_stmt":    ("#7f849c", "normal"),      # dim
    "ast_op":      ("#89b4fa", "normal"),      # blue
    "ast_assign":  ("#cba6f7", "normal"),      # purple
    "ast_call":    ("#89dceb", "bold"),        # cyan bold
    "ast_literal": ("#a6e3a1", "normal"),      # green
    "ast_ident":   ("#cdd6f4", "normal"),      # text
    "ast_error":   ("#f38ba8", "bold"),        # red
    "ast_meta":    ("#7f849c", "normal"),      # dim  (line info)
    "ast_tree":    ("#45475a", "normal"),      # tree lines
    "ast_prop":    ("#6c7086", "normal"),      # property labels
    "ast_propval": ("#a6e3a1", "normal"),      # property values
}


_AST_MAX_DEPTH   = 30    # safety limit
_AST_MAX_LIST    = 200   # max list children to expand
_SKIP_FIELDS     = {"line", "column"}   # always shown in node header
_COLLAPSE_NODES  = {"ExpressionStmt", "Block"}  # don't repeat label if boring


def _node_label(node) -> str:
    """One-line summary for an AST node."""
    cls = type(node).__name__
    parts = []
    # Include the most informative fields inline
    for attr in ("name", "language", "operator", "value",
                 "module", "iterator", "target", "literal_type", "member",
                 "error_type", "message", "token"):
        val = getattr(node, attr, None)
        if val not in (None, "", []):
            # Truncate long strings
            s = str(val)
            if len(s) > 40:
                s = s[:37] + "..."
            parts.append(f"{attr}={s!r}")
    suffix = "  " + ",  ".join(parts) if parts else ""
    line_info = ""
    if getattr(node, "line", 0):
        line_info = f"  [L{node.line}]"
    return cls, suffix, line_info


def render_ast_tree(root, language: str) -> list[tuple[str, str]]:
    """
    Walk the AST rooted at `root` and return a list of (text, tag) pairs
    ready for insertion into a tk.Text widget.
    """
    if root is None:
        return [("(No AST produced)\n", "ast_error")]

    lines: list[tuple[str, str]] = []

    # Header
    lines.append((f"  Abstract Syntax Tree  —  {language.upper()}\n", "ast_root"))
    lines.append(("  " + "─" * 54 + "\n", "ast_tree"))
    lines.append(("\n", ""))

    try:
        from syntax_tree.ast_nodes import ASTNode
    except Exception:
        lines.append(("  [Cannot import AST node classes]\n", "ast_error"))
        return lines

    def _recurse(node, prefix: str, is_last: bool, depth: int):
        if depth > _AST_MAX_DEPTH:
            lines.append((prefix + "  …\n", "ast_tree"))
            return
        if node is None:
            return
        if not isinstance(node, ASTNode):
            return

        connector = "└── " if is_last else "├── "
        child_pfx  = prefix + ("    " if is_last else "│   ")

        cls, suffix, line_info = _node_label(node)
        tag = _AST_NODE_TAGS.get(cls, "ast_stmt")

        # Tree connector in dim colour
        lines.append((prefix + connector, "ast_tree"))
        # Node class name in its colour
        lines.append((cls, tag))
        # Suffix (key attributes) in property-value colour
        if suffix:
            lines.append((suffix, "ast_propval"))
        # Line number in dim
        if line_info:
            lines.append((line_info, "ast_meta"))
        lines.append(("\n", ""))

        # Collect child fields (lists or ASTNode values)
        fields = []
        for fname, fval in vars(node).items():
            if fname in _SKIP_FIELDS:
                continue
            if fname in ("name", "language", "operator", "value",
                         "module", "iterator", "target", "literal_type",
                         "member", "error_type", "message", "token",
                         "return_type", "param_type", "var_type", "is_const",
                         "modifiers", "parent"):
                # Already shown inline in label or trivial scalars
                continue
            if isinstance(fval, ASTNode):
                fields.append((fname, [fval]))
            elif isinstance(fval, list) and fval:
                child_nodes = [x for x in fval if isinstance(x, ASTNode)]
                if child_nodes:
                    fields.append((fname, child_nodes))

        for fi, (fname, children) in enumerate(fields):
            f_is_last = (fi == len(fields) - 1)
            f_connector = "└── " if f_is_last else "├── "
            f_child_pfx = child_pfx + ("    " if f_is_last else "│   ")

            # Field label row
            lines.append((child_pfx + f_connector, "ast_tree"))
            lines.append((f"{fname}", "ast_prop"))
            if len(children) > 1:
                lines.append((f"  [{len(children)} items]", "ast_meta"))
            lines.append(("\n", ""))

            shown = children[:_AST_MAX_LIST]
            for ci, child in enumerate(shown):
                c_is_last = (ci == len(shown) - 1) and len(children) <= _AST_MAX_LIST
                _recurse(child, f_child_pfx, c_is_last, depth + 1)
            if len(children) > _AST_MAX_LIST:
                lines.append((f_child_pfx + f"  … ({len(children) - _AST_MAX_LIST} more)\n",
                              "ast_meta"))

    # Start recursion from root's children so the Program node is the first visible
    if hasattr(root, "statements") and root.statements:
        stmts = root.statements
        for i, stmt in enumerate(stmts):
            _recurse(stmt, "  ", i == len(stmts) - 1, 0)
    else:
        _recurse(root, "  ", True, 0)

    lines.append(("\n", ""))
    lines.append(("  " + "─" * 54 + "\n", "ast_tree"))
    return lines


# ════════════════════════════════════════════════════════════════════════════
# Custom Widgets
# ════════════════════════════════════════════════════════════════════════════

class HoverButton(tk.Button):
    """A tk.Button that changes colour on hover."""

    def __init__(self, master, hover_bg: str, normal_bg: str, **kwargs):
        super().__init__(master, bg=normal_bg, activebackground=hover_bg,
                         cursor="hand2", relief="flat", borderwidth=0, **kwargs)
        self._normal = normal_bg
        self._hover  = hover_bg
        self.bind("<Enter>", lambda _: self.config(bg=self._hover))
        self.bind("<Leave>", lambda _: self.config(bg=self._normal))


class LineNumberedText(tk.Frame):
    """A Text widget with a line-number gutter."""

    def __init__(self, master, **kwargs):
        super().__init__(master, bg=C["bg3"])
        text_kwargs = {k: v for k, v in kwargs.items()}

        # Gutter
        self._font = font.Font(family="Consolas", size=11)
        self.gutter = tk.Text(
            self, width=4, state="disabled", bg=C["lineno"],
            fg=C["text_dim"], font=self._font, relief="flat",
            padx=6, takefocus=False, cursor="arrow",
            selectbackground=C["lineno"], wrap="none",
        )
        self.gutter.pack(side="left", fill="y")

        # Separator line
        tk.Frame(self, bg=C["surface"], width=1).pack(side="left", fill="y")

        # Main text area
        self.text = tk.Text(
            self, bg=C["bg3"], fg=C["text"], insertbackground=C["accent"],
            font=self._font, relief="flat", padx=8, pady=4,
            selectbackground=C["surface"], wrap="none",
            undo=True, autoseparators=True, maxundo=-1,
            **text_kwargs,
        )
        # Horizontal scrollbar
        hbar = tk.Scrollbar(self, orient="horizontal",
                            command=self.text.xview, bg=C["bg2"])
        hbar.pack(side="bottom", fill="x")
        # Vertical scrollbar
        vbar = tk.Scrollbar(self, orient="vertical",
                            command=self._on_vscroll, bg=C["bg2"])
        vbar.pack(side="right", fill="y")

        self.text.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.text.pack(side="left", fill="both", expand=True)

        self.text.bind("<KeyRelease>", self._update)
        self.text.bind("<ButtonRelease>", self._update)
        self.text.bind("<MouseWheel>", self._on_mousewheel)
        self._update()

    # ── Scroll sync ──────────────────────────────────────────────────────────

    def _on_vscroll(self, *args):
        self.text.yview(*args)
        self._sync_gutter()

    def _on_mousewheel(self, event):
        self.text.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self._sync_gutter()

    def _sync_gutter(self):
        """Keep the gutter scrolled in sync with the text widget."""
        first = self.text.index("@0,0")
        self.gutter.config(state="normal")
        # Sync gutter view
        self.gutter.yview_moveto(self.text.yview()[0])
        self.gutter.config(state="disabled")

    # ── Line numbers ─────────────────────────────────────────────────────────

    def _update(self, *_):
        self._redraw_gutter()

    def _redraw_gutter(self):
        lines = int(self.text.index("end-1c").split(".")[0])
        self.gutter.config(state="normal")
        self.gutter.delete("1.0", "end")
        for i in range(1, lines + 1):
            self.gutter.insert("end", f"{i:>3}\n")
        self.gutter.config(state="disabled")
        self._sync_gutter()

    # ── Syntax highlighting ──────────────────────────────────────────────────

    def apply_python_highlighting(self):
        content = self.text.get("1.0", "end-1c")
        for tag in self.text.tag_names():
            if tag.startswith("hl_"):
                self.text.tag_remove(tag, "1.0", "end")
        for name, pattern in _PY_PATTERNS:
            tag = f"hl_{name}"
            color = _PY_COLORS.get(name, C["text"])
            self.text.tag_config(tag, foreground=color)
            for m in re.finditer(pattern, content, re.MULTILINE):
                # Use last group if capturing groups exist, else whole match
                start_char = m.start(len(m.groups())) if m.lastindex else m.start()
                end_char   = m.end(len(m.groups())) if m.lastindex else m.end()
                start_idx = f"1.0+{start_char}c"
                end_idx   = f"1.0+{end_char}c"
                self.text.tag_add(tag, start_idx, end_idx)

    # ── Public helpers ───────────────────────────────────────────────────────

    def get_content(self) -> str:
        return self.text.get("1.0", "end-1c")

    def set_content(self, text: str):
        self.text.delete("1.0", "end")
        self.text.insert("1.0", text)
        self._update()

    def clear(self):
        self.text.delete("1.0", "end")
        self._update()


# ════════════════════════════════════════════════════════════════════════════
# Main Application
# ════════════════════════════════════════════════════════════════════════════

class SyntaxAnalyzerGUI(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("ML-Powered Syntax Error Analyzer")
        self.geometry("1300x820")
        self.minsize(900, 600)
        self.configure(bg=C["bg"])

        # Try to set a window icon (silently ignore if unavailable)
        try:
            self.iconbitmap(default="")
        except Exception:
            pass

        self._language = "python"  # fixed — Python only
        self._status_text = tk.StringVar(value="Ready — paste your code and click  Analyze Code")
        self._busy = False
        self._report_data = None
        self._last_source = ""        # source code from last successful analysis
        self._can_run = False          # True when last analysis had 0 blocking errors

        self._setup_styles()
        self._build_ui()
        self._render_report_tabs(None)
        self._load_sample()

    # ── Styles ───────────────────────────────────────────────────────────────

    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook",         background=C["bg2"], borderwidth=0)
        style.configure("TNotebook.Tab",
                        background=C["tab_inactive"], foreground=C["text_dim"],
                        padding=[16, 8], font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab",
                  background=[("selected", C["tab_active"])],
                  foreground=[("selected", C["text"])])
        style.configure("Vertical.TScrollbar",  background=C["bg2"],
                        troughcolor=C["bg3"], borderwidth=0)
        style.configure("Horizontal.TScrollbar", background=C["bg2"],
                        troughcolor=C["bg3"], borderwidth=0)
        style.configure("TFrame", background=C["bg"])
        style.configure("TLabel", background=C["bg"], foreground=C["text"])

    # ── UI Construction ──────────────────────────────────────────────────────

    def _build_ui(self):
        # ── Top title bar ─────────────────────────────────────────────────
        title_bar = tk.Frame(self, bg=C["bg2"], height=56)
        title_bar.pack(fill="x", side="top")
        title_bar.pack_propagate(False)

        tk.Label(
            title_bar,
            text="⚡  ML-Powered Syntax Error Analyzer",
            bg=C["bg2"], fg=C["accent"],
            font=("Segoe UI", 16, "bold"),
        ).pack(side="left", padx=20, pady=12)

        # Static language badge — Python only
        tk.Label(
            title_bar, text="🐍  Python",
            bg=C["bg2"], fg=C["accent2"],
            font=("Segoe UI", 10, "bold"),
        ).pack(side="right", padx=20, pady=14)

        # ── Main paned area ───────────────────────────────────────────────
        paned = tk.PanedWindow(
            self, orient="horizontal", bg=C["surface"],
            sashwidth=5, sashrelief="flat", handlesize=0,
        )
        paned.pack(fill="both", expand=True, padx=0, pady=0)

        # Left panel: code editor
        left = tk.Frame(paned, bg=C["bg"])
        paned.add(left, minsize=400, width=600)

        # Editor header
        editor_header = tk.Frame(left, bg=C["bg2"], height=40)
        editor_header.pack(fill="x")
        editor_header.pack_propagate(False)
        tk.Label(
            editor_header, text="  📝  Code Editor",
            bg=C["bg2"], fg=C["text"], font=("Segoe UI", 10, "bold"),
        ).pack(side="left", padx=8, pady=8)

        # Open-file button
        HoverButton(
            editor_header, text="📂  Open File",
            hover_bg=C["btn2_hover"], normal_bg=C["btn2_bg"],
            fg=C["text"], font=("Segoe UI", 9),
            command=self._open_file, padx=8, pady=4,
        ).pack(side="right", padx=4, pady=5)

        # Editor area
        self.editor = LineNumberedText(left)
        self.editor.pack(fill="both", expand=True, padx=0, pady=0)
        # Live syntax highlighting
        self.editor.text.bind("<KeyRelease>", self._on_key_release)

        # Action buttons
        btn_bar = tk.Frame(left, bg=C["bg2"], height=52)
        btn_bar.pack(fill="x")
        btn_bar.pack_propagate(False)

        self._analyze_btn = HoverButton(
            btn_bar, text="▶  Analyze Code",
            hover_bg=C["btn_hover"], normal_bg=C["btn_bg"],
            fg=C["btn_fg"], font=("Segoe UI", 11, "bold"),
            command=self._analyze, padx=20, pady=8,
        )
        self._analyze_btn.pack(side="left", padx=12, pady=8)

        # ── Run Code button (enabled only after clean analysis) ───────────
        self._run_btn = HoverButton(
            btn_bar, text="▶▶  Run Code",
            hover_bg="#15803d", normal_bg="#16a34a",
            fg="#ffffff", font=("Segoe UI", 11, "bold"),
            command=self._run_code, padx=16, pady=8,
            state="disabled",
        )
        self._run_btn.pack(side="left", padx=4, pady=8)

        HoverButton(
            btn_bar, text="🗑  Clear Editor",
            hover_bg=C["btn2_hover"], normal_bg=C["btn2_bg"],
            fg=C["btn2_fg"], font=("Segoe UI", 10),
            command=self._clear_editor, padx=14, pady=8,
        ).pack(side="left", padx=4, pady=8)

        HoverButton(
            btn_bar, text="💡  Load Sample",
            hover_bg=C["btn2_hover"], normal_bg=C["btn2_bg"],
            fg=C["btn2_fg"], font=("Segoe UI", 10),
            command=self._load_sample, padx=14, pady=8,
        ).pack(side="left", padx=4, pady=8)

        # Right panel: tabbed notebook (Diagnostics + AST View)
        right = tk.Frame(paned, bg=C["bg"])
        paned.add(right, minsize=350)

        # Top toolbar (Copy / Save — apply to whichever tab is active)
        results_header = tk.Frame(right, bg=C["bg2"], height=40)
        results_header.pack(fill="x")
        results_header.pack_propagate(False)
        tk.Label(
            results_header, text="  📊  Analysis Results",
            bg=C["bg2"], fg=C["text"], font=("Segoe UI", 10, "bold"),
        ).pack(side="left", padx=8, pady=8)
        HoverButton(
            results_header, text="📋  Copy",
            hover_bg=C["btn2_hover"], normal_bg=C["btn2_bg"],
            fg=C["text"], font=("Segoe UI", 9),
            command=self._copy_results, padx=8, pady=4,
        ).pack(side="right", padx=4, pady=5)
        HoverButton(
            results_header, text="💾  Save Report",
            hover_bg=C["btn2_hover"], normal_bg=C["btn2_bg"],
            fg=C["text"], font=("Segoe UI", 9),
            command=self._save_report, padx=8, pady=4,
        ).pack(side="right", padx=4, pady=5)

        # Notebook
        self._notebook = ttk.Notebook(right)
        self._notebook.pack(fill="both", expand=True)

        # ── Tab 1: Diagnostics ────────────────────────────────────────────
        diag_frame = tk.Frame(self._notebook, bg=C["bg2"])
        self._notebook.add(diag_frame, text="  📋  Diagnostics  ")

        self.results = tk.Text(
            diag_frame, bg=C["bg2"], fg=C["text"],
            font=("Consolas", 10), relief="flat",
            padx=10, pady=8, state="disabled",
            selectbackground=C["surface"], wrap="none",
        )
        vbar_r = tk.Scrollbar(diag_frame, orient="vertical",
                              command=self.results.yview, bg=C["bg2"])
        hbar_r = tk.Scrollbar(diag_frame, orient="horizontal",
                              command=self.results.xview, bg=C["bg2"])
        self.results.config(yscrollcommand=vbar_r.set,
                            xscrollcommand=hbar_r.set)
        hbar_r.pack(side="bottom", fill="x")
        vbar_r.pack(side="right",  fill="y")
        self.results.pack(fill="both", expand=True)

        # Configure result text tags for coloured output
        self.results.tag_config("header",   foreground=C["accent"],  font=("Consolas", 10, "bold"))
        self.results.tag_config("ok",       foreground=C["accent3"])
        self.results.tag_config("error",    foreground=C["error"])
        self.results.tag_config("warning",  foreground=C["warn"])
        self.results.tag_config("info",     foreground=C["info"])
        self.results.tag_config("title",    foreground=C["accent2"], font=("Consolas", 10, "bold"))
        self.results.tag_config("fix",      foreground=C["accent3"])
        self.results.tag_config("srcline",  foreground=C["text"])
        self.results.tag_config("caret",    foreground=C["error"])
        self.results.tag_config("dim",      foreground=C["text_dim"])

        # ── Tab 2: AST View ───────────────────────────────────────────────
        ast_frame = tk.Frame(self._notebook, bg=C["bg2"])
        self._notebook.add(ast_frame, text="  🌳  AST View  ")

        self.ast_view = tk.Text(
            ast_frame, bg=C["bg2"], fg=C["text"],
            font=("Consolas", 10), relief="flat",
            padx=10, pady=8, state="disabled",
            selectbackground=C["surface"], wrap="none",
        )
        vbar_a = tk.Scrollbar(ast_frame, orient="vertical",
                              command=self.ast_view.yview, bg=C["bg2"])
        hbar_a = tk.Scrollbar(ast_frame, orient="horizontal",
                              command=self.ast_view.xview, bg=C["bg2"])
        self.ast_view.config(yscrollcommand=vbar_a.set,
                             xscrollcommand=hbar_a.set)
        hbar_a.pack(side="bottom", fill="x")
        vbar_a.pack(side="right",  fill="y")
        self.ast_view.pack(fill="both", expand=True)

        # Configure AST colour tags
        for _tag, (_color, _weight) in _AST_TAG_COLORS.items():
            self.ast_view.tag_config(
                _tag,
                foreground=_color,
                font=("Consolas", 10, _weight),
            )

        # ── Tab 3: IR View ────────────────────────────────────
        ir_frame = tk.Frame(self._notebook, bg=C["bg2"])
        self._notebook.add(ir_frame, text="  🔬  IR View  ")

        self.ir_view = tk.Text(
            ir_frame, bg=C["bg2"], fg=C["text"],
            font=("Consolas", 10), relief="flat",
            padx=10, pady=8, state="disabled",
            selectbackground=C["surface"], wrap="none",
        )
        vbar_ir = tk.Scrollbar(ir_frame, orient="vertical",
                               command=self.ir_view.yview, bg=C["bg2"])
        hbar_ir = tk.Scrollbar(ir_frame, orient="horizontal",
                               command=self.ir_view.xview, bg=C["bg2"])
        self.ir_view.config(yscrollcommand=vbar_ir.set, xscrollcommand=hbar_ir.set)
        hbar_ir.pack(side="bottom", fill="x")
        vbar_ir.pack(side="right",  fill="y")
        self.ir_view.pack(fill="both", expand=True)

        # IR text colour tags
        self.ir_view.tag_config("ir_header",  foreground=C["accent"],  font=("Consolas", 10, "bold"))
        self.ir_view.tag_config("ir_block",   foreground=C["accent2"], font=("Consolas", 10, "bold"))
        self.ir_view.tag_config("ir_instr",   foreground=C["text"])
        self.ir_view.tag_config("ir_op",      foreground=C["info"])
        self.ir_view.tag_config("ir_edge",    foreground=C["text_dim"])
        self.ir_view.tag_config("ir_summary", foreground=C["accent3"])

        security_frame = tk.Frame(self._notebook, bg=C["bg2"])
        self._notebook.add(security_frame, text="  Security Report  ")

        self.security_view = tk.Text(
            security_frame, bg=C["bg2"], fg=C["text"],
            font=("Consolas", 10), relief="flat",
            padx=10, pady=8, state="disabled",
            selectbackground=C["surface"], wrap="word",
        )
        vbar_sec = tk.Scrollbar(security_frame, orient="vertical",
                                command=self.security_view.yview, bg=C["bg2"])
        self.security_view.config(yscrollcommand=vbar_sec.set)
        vbar_sec.pack(side="right", fill="y")
        self.security_view.pack(fill="both", expand=True)

        current_frame = tk.Frame(self._notebook, bg=C["bg2"])
        self._notebook.add(current_frame, text="  ⚡  Current Report  ")

        # Scrollable container for the Current Report tab
        cur_scroll_canvas = tk.Canvas(current_frame, bg=C["bg"],
                                      highlightthickness=0)
        cur_vbar = tk.Scrollbar(current_frame, orient="vertical",
                                command=cur_scroll_canvas.yview)
        cur_scroll_canvas.configure(yscrollcommand=cur_vbar.set)
        cur_vbar.pack(side="right", fill="y")
        cur_scroll_canvas.pack(side="left", fill="both", expand=True)

        cur_inner = tk.Frame(cur_scroll_canvas, bg=C["bg"])
        cur_inner_id = cur_scroll_canvas.create_window((0, 0), window=cur_inner,
                                                        anchor="nw")

        def _cur_configure(event):
            cur_scroll_canvas.configure(
                scrollregion=cur_scroll_canvas.bbox("all"))
            cur_scroll_canvas.itemconfig(
                cur_inner_id, width=cur_scroll_canvas.winfo_width())
        cur_inner.bind("<Configure>", _cur_configure)
        cur_scroll_canvas.bind("<Configure>",
            lambda e: cur_scroll_canvas.itemconfig(
                cur_inner_id, width=e.width))
        cur_scroll_canvas.bind_all("<MouseWheel>",
            lambda e: cur_scroll_canvas.yview_scroll(
                int(-1 * (e.delta / 120)), "units"))

        # Summary card panel (dynamic widgets added at render time)
        self.current_summary_frame = tk.Frame(cur_inner, bg=C["bg"])
        self.current_summary_frame.pack(fill="x", padx=10, pady=(10, 4))

        # Charts
        self.current_loc_canvas = tk.Canvas(
            cur_inner, bg="#ffffff", highlightthickness=1,
            highlightbackground=C["surface"], height=320,
        )
        self.current_loc_canvas.pack(fill="x", padx=10, pady=(4, 6))

        self.current_hotspot_canvas = tk.Canvas(
            cur_inner, bg="#ffffff", highlightthickness=1,
            highlightbackground=C["surface"], height=320,
        )
        self.current_hotspot_canvas.pack(fill="x", padx=10, pady=(0, 10))

        cumulative_frame = tk.Frame(self._notebook, bg=C["bg2"])
        self._notebook.add(cumulative_frame, text="  📈  Cumulative Report  ")

        # Scrollable container for the Cumulative Report tab
        cum_scroll_canvas = tk.Canvas(cumulative_frame, bg=C["bg"],
                                       highlightthickness=0)
        cum_vbar = tk.Scrollbar(cumulative_frame, orient="vertical",
                                command=cum_scroll_canvas.yview)
        cum_scroll_canvas.configure(yscrollcommand=cum_vbar.set)
        cum_vbar.pack(side="right", fill="y")
        cum_scroll_canvas.pack(side="left", fill="both", expand=True)

        cum_inner = tk.Frame(cum_scroll_canvas, bg=C["bg"])
        cum_inner_id = cum_scroll_canvas.create_window((0, 0), window=cum_inner,
                                                        anchor="nw")

        def _cum_configure(event):
            cum_scroll_canvas.configure(
                scrollregion=cum_scroll_canvas.bbox("all"))
            cum_scroll_canvas.itemconfig(
                cum_inner_id, width=cum_scroll_canvas.winfo_width())
        cum_inner.bind("<Configure>", _cum_configure)
        cum_scroll_canvas.bind("<Configure>",
            lambda e: cum_scroll_canvas.itemconfig(
                cum_inner_id, width=e.width))

        # Summary card panel
        self.cumulative_summary_frame = tk.Frame(cum_inner, bg=C["bg"])
        self.cumulative_summary_frame.pack(fill="x", padx=10, pady=(10, 4))

        # Charts
        self.energy_trend_canvas = tk.Canvas(
            cum_inner, bg="#ffffff", highlightthickness=1,
            highlightbackground=C["surface"], height=320,
        )
        self.energy_trend_canvas.pack(fill="x", padx=10, pady=(4, 6))

        self.cumulative_loc_canvas = tk.Canvas(
            cum_inner, bg="#ffffff", highlightthickness=1,
            highlightbackground=C["surface"], height=320,
        )
        self.cumulative_loc_canvas.pack(fill="x", padx=10, pady=(0, 10))

        # Hidden text widgets kept for copy/save compatibility (not displayed)
        self.current_report_text = tk.Text(current_frame, height=1, state="disabled")
        self.cumulative_report_text = tk.Text(cumulative_frame, height=1, state="disabled")

        # ── Tab 7: Carbon & Power Report ──────────────────────────────────
        carbon_frame = tk.Frame(self._notebook, bg=C["bg2"])
        self._notebook.add(carbon_frame, text="  🌱  Carbon & Power  ")

        # Scrollable container
        cp_scroll_cv = tk.Canvas(carbon_frame, bg="#0f1117", highlightthickness=0)
        cp_vbar = tk.Scrollbar(carbon_frame, orient="vertical",
                               command=cp_scroll_cv.yview)
        cp_scroll_cv.configure(yscrollcommand=cp_vbar.set)
        cp_vbar.pack(side="right", fill="y")
        cp_scroll_cv.pack(side="left", fill="both", expand=True)

        self._carbon_inner = tk.Frame(cp_scroll_cv, bg="#0f1117")
        _cp_win_id = cp_scroll_cv.create_window((0, 0), window=self._carbon_inner, anchor="nw")

        def _cp_cfg(e):
            cp_scroll_cv.configure(scrollregion=cp_scroll_cv.bbox("all"))
            cp_scroll_cv.itemconfig(_cp_win_id, width=cp_scroll_cv.winfo_width())
        self._carbon_inner.bind("<Configure>", _cp_cfg)
        cp_scroll_cv.bind("<Configure>",
            lambda e: cp_scroll_cv.itemconfig(_cp_win_id, width=e.width))

        # Placeholder message (replaced after analysis)
        self._carbon_placeholder = tk.Label(
            self._carbon_inner,
            text="Run an analysis to see Carbon & Power metrics.",
            bg="#0f1117", fg="#6e7681",
            font=("Segoe UI", 12), anchor="center",
        )
        self._carbon_placeholder.pack(expand=True, pady=60)

        # ── Tab 8: Execution Output ────────────────────────────────────────
        exec_frame = tk.Frame(self._notebook, bg=C["bg2"])
        self._notebook.add(exec_frame, text="  ▶  Execution  ")

        # Execution toolbar
        exec_toolbar = tk.Frame(exec_frame, bg=C["bg"], height=40)
        exec_toolbar.pack(fill="x")
        exec_toolbar.pack_propagate(False)
        tk.Label(
            exec_toolbar, text="  ▶  Program Execution Output",
            bg=C["bg"], fg=C["accent3"], font=("Segoe UI", 10, "bold"),
        ).pack(side="left", padx=8, pady=8)
        self._exec_status_label = tk.Label(
            exec_toolbar, text="Run Code to see output",
            bg=C["bg"], fg=C["text_dim"], font=("Segoe UI", 9),
        )
        self._exec_status_label.pack(side="right", padx=12, pady=8)

        self.exec_view = tk.Text(
            exec_frame, bg="#0d1117", fg="#e6edf3",
            font=("Consolas", 11), relief="flat",
            padx=12, pady=10, state="disabled",
            selectbackground="#264f78", wrap="word",
            insertbackground="#58a6ff",
        )
        vbar_exec = tk.Scrollbar(exec_frame, orient="vertical",
                                  command=self.exec_view.yview, bg=C["bg2"])
        hbar_exec = tk.Scrollbar(exec_frame, orient="horizontal",
                                  command=self.exec_view.xview, bg=C["bg2"])
        self.exec_view.config(yscrollcommand=vbar_exec.set,
                               xscrollcommand=hbar_exec.set)
        hbar_exec.pack(side="bottom", fill="x")
        vbar_exec.pack(side="right",  fill="y")
        self.exec_view.pack(fill="both", expand=True)

        # Execution text colour tags
        self.exec_view.tag_config("exec_header",  foreground="#58a6ff",  font=("Consolas", 11, "bold"))
        self.exec_view.tag_config("exec_stdout",  foreground="#e6edf3")
        self.exec_view.tag_config("exec_stderr",  foreground="#ff7b72",  font=("Consolas", 11, "bold"))
        self.exec_view.tag_config("exec_input",   foreground="#3fb950",  font=("Consolas", 11, "bold"))
        self.exec_view.tag_config("exec_ok",      foreground="#3fb950",  font=("Consolas", 11, "bold"))
        self.exec_view.tag_config("exec_fail",    foreground="#ff7b72",  font=("Consolas", 11, "bold"))
        self.exec_view.tag_config("exec_dim",     foreground="#6e7681")
        self.exec_view.tag_config("exec_sep",     foreground="#30363d")

        # ── Status bar ────────────────────────────────────────────────────
        self._status_bar = tk.Frame(self, bg=C["bg2"], height=32)
        self._status_bar.pack(fill="x", side="bottom")
        self._status_bar.pack_propagate(False)

        # Animated spinner label
        self._spinner_label = tk.Label(
            self._status_bar, text="", bg=C["bg2"],
            fg=C["accent"], font=("Segoe UI", 11),
        )
        self._spinner_label.pack(side="left", padx=10, pady=4)

        self._status_label = tk.Label(
            self._status_bar, textvariable=self._status_text,
            bg=C["bg2"], fg=C["text_dim"],
            font=("Segoe UI", 9), anchor="w",
        )
        self._status_label.pack(side="left", fill="x", expand=True, pady=5)

        self._error_count_label = tk.Label(
            self._status_bar, text="",
            bg=C["bg2"], fg=C["text_dim"],
            font=("Segoe UI", 9, "bold"),
        )
        self._error_count_label.pack(side="right", padx=16, pady=5)

        # Progress / busy indicator
        self._progress = ttk.Progressbar(
            self._status_bar, mode="indeterminate", length=100,
        )

    # ── Event handlers ───────────────────────────────────────────────────────

    def _on_key_release(self, event=None):
        # Always Python — apply syntax highlighting on every key
        self.editor.apply_python_highlighting()
        self.editor._update()

    def _open_file(self):
        path = filedialog.askopenfilename(
            title="Open Python file",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")],
        )
        if path:
            try:
                with open(path, encoding="utf-8", errors="replace") as fh:
                    content = fh.read()
                self.editor.set_content(content)
                self.editor.apply_python_highlighting()
                self._status_text.set(f"Loaded: {os.path.basename(path)}")
            except Exception as exc:
                messagebox.showerror("File Error", str(exc))

    def _clear_editor(self):
        self.editor.clear()
        self._clear_results()
        self._status_text.set("Editor cleared.")
        self._error_count_label.config(text="", fg=C["text_dim"])

    def _load_sample(self):
        self.editor.set_content(_SAMPLES.get("python", ""))
        self.editor.apply_python_highlighting()
        self._status_text.set("Loaded sample Python code with intentional errors.")

    def _clear_results(self):
        self.results.config(state="normal")
        self.results.delete("1.0", "end")
        self.results.config(state="disabled")
        self.ast_view.config(state="normal")
        self.ast_view.delete("1.0", "end")
        self.ast_view.config(state="disabled")
        self.ir_view.config(state="normal")
        self.ir_view.delete("1.0", "end")
        self.ir_view.config(state="disabled")
        self.security_view.config(state="normal")
        self.security_view.delete("1.0", "end")
        self.security_view.config(state="disabled")
        self.current_report_text.config(state="normal")
        self.current_report_text.delete("1.0", "end")
        self.current_report_text.config(state="disabled")
        self.cumulative_report_text.config(state="normal")
        self.cumulative_report_text.delete("1.0", "end")
        self.cumulative_report_text.config(state="disabled")
        self.exec_view.config(state="normal")
        self.exec_view.delete("1.0", "end")
        self.exec_view.config(state="disabled")
        self._exec_status_label.config(text="Run Code to see output", fg=C["text_dim"])
        # Reset carbon panel
        for w in self._carbon_inner.winfo_children():
            w.destroy()
        self._carbon_placeholder = tk.Label(
            self._carbon_inner,
            text="Run an analysis to see Carbon & Power metrics.",
            bg="#0f1117", fg="#6e7681",
            font=("Segoe UI", 12), anchor="center",
        )
        self._carbon_placeholder.pack(expand=True, pady=60)
        self._clear_frame(self.current_summary_frame)
        self._clear_frame(self.cumulative_summary_frame)
        for canvas in (
            self.current_loc_canvas,
            self.current_hotspot_canvas,
            self.energy_trend_canvas,
            self.cumulative_loc_canvas,
        ):
            canvas.delete("all")
        self._report_data = None
        # Disable run button when results are cleared
        self._can_run = False
        self._last_source = ""
        self._run_btn.config(
            state="disabled",
            bg="#16a34a",
            text="▶▶  Run Code",
        )

    # ── Analysis ─────────────────────────────────────────────────────────────

    def _analyze(self):
        if self._busy:
            return
        source = self.editor.get_content().strip()
        if not source:
            messagebox.showwarning("Empty Editor", "Please paste or type some code first.")
            return

        self._busy = True
        self._analyze_btn.config(state="disabled", text="⏳  Analyzing…")
        self._status_text.set("Running analysis…")
        self._error_count_label.config(text="", fg=C["text_dim"])
        self._clear_results()
        self._progress.pack(side="right", padx=10, pady=6)
        self._progress.start(12)

        # Run in a background thread to keep the GUI responsive
        _source = source  # capture for closure
        def _worker():
            output    = run_analysis(_source, "python")
            payload = build_report_payload(_source, "python")
            ast_lines = render_ast_tree(payload["ast_root"], "python")
            ir_lines  = _render_ir_program_view(payload["ir_program"])
            security_report = None
            try:
                from analysis.security_vulnerability import build_security_report
                security_report = build_security_report(payload["ast_root"])
            except Exception:
                security_report = None
            report_data = None
            try:
                from analysis.performance_energy import build_reports
                report_data = build_reports(
                    source=_source,
                    language="python",
                    filepath="<editor>",
                    ast_tree=payload["ast_root"],
                    ir_program=payload["ir_program"],
                    errors=payload["errors"],
                    timing_breakdown=payload["timing"],
                    persist=True,
                )
            except Exception:
                report_data = None
            self.after(0, lambda: self._display_results(output, ast_lines, ir_lines, report_data, security_report, _source))

        threading.Thread(target=_worker, daemon=True).start()

    def _display_results(self, output: str, ast_lines: list, ir_lines: list, report_data: dict | None, security_report: dict | None, source: str = ""):
        """Called on the main thread after analysis completes."""
        self._progress.stop()
        self._progress.pack_forget()
        self._analyze_btn.config(state="normal", text="▶  Analyze Code")
        self._busy = False

        n_errors = count_errors(output)

        if n_errors == 0:
            self._status_label.config(fg=C["status_ok"])
            self._status_text.set("✓  Analysis complete — No errors found! Click  ▶▶ Run Code  to execute.")
            self._error_count_label.config(
                text="✓  Clean", fg=C["status_ok"])
            # Enable execution mode
            self._can_run = True
            self._last_source = source
            self._run_btn.config(
                state="normal",
                bg="#16a34a",
                text="▶▶  Run Code",
            )
        else:
            self._status_label.config(fg=C["status_err"])
            self._status_text.set(f"✗  Analysis complete — {n_errors} error(s) detected. Fix errors before running.")
            self._error_count_label.config(
                text=f"✗  {n_errors} Error{'s' if n_errors != 1 else ''}",
                fg=C["status_err"],
            )
            # Disable execution mode
            self._can_run = False
            self._last_source = ""
            self._run_btn.config(
                state="disabled",
                bg="#16a34a",
                text="▶▶  Run Code",
            )

        # ── Diagnostics tab ───────────────────────────────────────────────
        self.results.config(state="normal")
        self.results.delete("1.0", "end")
        for line in output.splitlines(keepends=True):
            tag = self._classify_line(line)
            self.results.insert("end", line, tag)
        self.results.config(state="disabled")
        self.results.see("1.0")

        # ── AST tab ───────────────────────────────────────────────────────
        self.ast_view.config(state="normal")
        self.ast_view.delete("1.0", "end")
        for text_chunk, tag in ast_lines:
            if tag:
                self.ast_view.insert("end", text_chunk, tag)
            else:
                self.ast_view.insert("end", text_chunk)
        self.ast_view.config(state="disabled")
        self.ast_view.see("1.0")

        # ── IR View tab ─────────────────────────────────────────────
        self.ir_view.config(state="normal")
        self.ir_view.delete("1.0", "end")
        for text_chunk, tag in ir_lines:
            if tag:
                self.ir_view.insert("end", text_chunk, tag)
            else:
                self.ir_view.insert("end", text_chunk)
        self.ir_view.config(state="disabled")
        self.ir_view.see("1.0")
        self.security_view.config(state="normal")
        self.security_view.delete("1.0", "end")
        self.security_view.insert("1.0", (security_report or {}).get("summary", "Security report unavailable."))
        self.security_view.config(state="disabled")
        self.security_view.see("1.0")
        self._render_report_tabs(report_data)
        # Render Carbon & Power panel
        self._render_carbon_panel(report_data)

    def _set_text_content(self, widget: tk.Text, text: str):
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", text)
        widget.config(state="disabled")
        widget.see("1.0")

    def _clear_frame(self, frame: tk.Frame):
        for child in frame.winfo_children():
            child.destroy()

    def _parse_summary_text(self, text: str):
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        title = lines[0] if lines else "Report"
        metrics = []
        sections = {}
        current_section = "Details"

        for line in lines[1:]:
            if line.endswith(":") and ": " not in line:
                current_section = line[:-1]
                sections.setdefault(current_section, [])
                continue
            if line.startswith("- "):
                sections.setdefault(current_section, []).append(line[2:])
                continue
            if ": " in line:
                key, value = line.split(": ", 1)
                metrics.append((key, value))
                continue
            sections.setdefault(current_section, []).append(line)

        return title, metrics, sections

    def _make_summary_card(self, parent: tk.Frame, key: str, value: str, accent: str):
        card = tk.Frame(parent, bg="#ffffff", highlightthickness=1, highlightbackground=C["surface"])
        top = tk.Frame(card, bg=accent, height=4)
        top.pack(fill="x", side="top")
        body = tk.Frame(card, bg="#ffffff")
        body.pack(fill="both", expand=True, padx=14, pady=12)

        tk.Label(
            body, text=key.upper(), bg="#ffffff", fg=C["text_dim"],
            font=("Segoe UI", 8, "bold"), anchor="w",
        ).pack(anchor="w")
        tk.Label(
            body, text=value, bg="#ffffff", fg=C["text"],
            font=("Segoe UI", 13, "bold"), anchor="w", justify="left", wraplength=220,
        ).pack(anchor="w", pady=(6, 0))
        return card

    def _render_summary_panel(self, frame: tk.Frame, text: str, accent: str):
        self._clear_frame(frame)
        title, metrics, sections = self._parse_summary_text(text)

        hero = tk.Frame(frame, bg="#ffffff", highlightthickness=1, highlightbackground=C["surface"])
        hero.pack(fill="x")
        hero_bar = tk.Frame(hero, bg=accent, height=5)
        hero_bar.pack(fill="x", side="top")
        hero_body = tk.Frame(hero, bg="#ffffff")
        hero_body.pack(fill="x", padx=16, pady=14)

        tk.Label(
            hero_body, text=title, bg="#ffffff", fg=C["text"],
            font=("Segoe UI", 16, "bold"), anchor="w",
        ).pack(anchor="w")
        tk.Label(
            hero_body, text="Overview of the latest analysis results",
            bg="#ffffff", fg=C["text_dim"], font=("Segoe UI", 9), anchor="w",
        ).pack(anchor="w", pady=(4, 0))

        cards_host = tk.Frame(frame, bg=C["bg"])
        cards_host.pack(fill="x", pady=(10, 8))
        for col in range(3):
            cards_host.grid_columnconfigure(col, weight=1)

        for idx, (key, value) in enumerate(metrics[:6]):
            card = self._make_summary_card(cards_host, key, value, accent)
            card.grid(row=idx // 3, column=idx % 3, sticky="nsew", padx=6, pady=6)

        remaining_metrics = metrics[6:]
        detail_lines = [f"{key}: {value}" for key, value in remaining_metrics]
        for section_name, items in sections.items():
            if items:
                detail_lines.append(f"{section_name}:")
                detail_lines.extend([f"- {item}" for item in items])

        if detail_lines:
            detail_card = tk.Frame(frame, bg="#ffffff", highlightthickness=1, highlightbackground=C["surface"])
            detail_card.pack(fill="x", pady=(2, 0))
            tk.Label(
                detail_card, text="Details", bg="#ffffff", fg=C["text"],
                font=("Segoe UI", 11, "bold"), anchor="w",
            ).pack(anchor="w", padx=16, pady=(12, 2))
            tk.Label(
                detail_card, text="\n".join(detail_lines), bg="#ffffff", fg=C["text_dim"],
                font=("Segoe UI", 9), anchor="w", justify="left", wraplength=980,
            ).pack(anchor="w", padx=16, pady=(0, 12))

    def _draw_placeholder(self, canvas: tk.Canvas, title: str, message: str):
        canvas.delete("all")
        width = max(canvas.winfo_width(), 320)
        height = max(canvas.winfo_height(), 200)
        canvas.create_rectangle(0, 0, width, height, fill="#ffffff", outline="", width=0)
        canvas.create_rectangle(4, 4, width - 4, height - 4, fill="#ffffff", outline=C["surface"], width=1)
        canvas.create_rectangle(4, 4, width - 4, 42, fill="#f8fbff", outline="")
        canvas.create_text(20, 23, anchor="w", text=title,
                           fill=C["text"], font=("Segoe UI", 12, "bold"))
        canvas.create_text(width / 2, height / 2, text=message,
                           fill=C["text_dim"], font=("Segoe UI", 10),
                           width=width - 40, justify="center")

    def _draw_line_chart(self, canvas: tk.Canvas, title: str, points: list, color: str):
        canvas.delete("all")
        width = max(canvas.winfo_width(), 520)
        height = max(canvas.winfo_height(), 260)
        canvas.create_rectangle(0, 0, width, height, fill="#ffffff", outline="", width=0)
        canvas.create_rectangle(4, 4, width - 4, height - 4, fill="#ffffff", outline=C["surface"], width=1)
        canvas.create_rectangle(4, 4, width - 4, 44, fill="#f8fbff", outline="")
        canvas.create_text(20, 24, anchor="w", text=title,
                           fill=C["text"], font=("Segoe UI", 12, "bold"))

        if not points:
            self._draw_placeholder(canvas, title, "No data available yet.")
            return

        left, top, right, bottom = 72, 64, width - 28, height - 46
        max_y = max(float(p.get("value", 0.0)) for p in points)
        max_y = max(max_y, 1.0)
        min_x = min(float(p.get("x", idx + 1)) for idx, p in enumerate(points))
        max_x = max(float(p.get("x", idx + 1)) for idx, p in enumerate(points))
        span_x = max(max_x - min_x, 1.0)

        for step in range(5):
            value = max_y * step / 4
            y = bottom - ((value / max_y) * (bottom - top))
            canvas.create_line(left, y, right, y, fill=C["surface"])
            canvas.create_text(18, y, anchor="w", text=f"{value:.2f}",
                               fill=C["text_dim"], font=("Segoe UI", 9))

        canvas.create_line(left, top, left, bottom, fill=C["text_dim"], width=1)
        canvas.create_line(left, bottom, right, bottom, fill=C["text_dim"], width=1)

        coords = []
        for idx, point in enumerate(points):
            x_val = float(point.get("x", idx + 1))
            y_val = float(point.get("value", 0.0))
            x = left + ((x_val - min_x) / span_x) * (right - left)
            y = bottom - ((y_val / max_y) * (bottom - top))
            coords.extend([x, y])
            canvas.create_line(x, y, x, bottom, fill="#e8eef7", dash=(2, 3))
            canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color, outline="#ffffff", width=2)
            canvas.create_text(x, bottom + 18, text=str(point.get("label", idx + 1)),
                               fill=C["text_dim"], font=("Segoe UI", 9))
        if len(coords) >= 4:
            canvas.create_line(*coords, fill=color, width=3)

    def _draw_bar_chart(self, canvas: tk.Canvas, title: str, items: list, color: str):
        canvas.delete("all")
        width = max(canvas.winfo_width(), 520)
        height = max(canvas.winfo_height(), 260)
        canvas.create_rectangle(0, 0, width, height, fill="#ffffff", outline="", width=0)
        canvas.create_rectangle(4, 4, width - 4, height - 4, fill="#ffffff", outline=C["surface"], width=1)
        canvas.create_rectangle(4, 4, width - 4, 44, fill="#f8fbff", outline="")
        canvas.create_text(20, 24, anchor="w", text=title,
                           fill=C["text"], font=("Segoe UI", 12, "bold"))

        if not items:
            self._draw_placeholder(canvas, title, "No data available yet.")
            return

        left, top, right, bottom = 72, 64, width - 28, height - 58
        max_y = max(float(item.get("value", 0.0)) for item in items)
        max_y = max(max_y, 1.0)
        count = len(items)
        gap = 18
        bar_w = max((right - left - gap * (count + 1)) / max(count, 1), 18)

        for step in range(5):
            value = max_y * step / 4
            y = bottom - ((value / max_y) * (bottom - top))
            canvas.create_line(left, y, right, y, fill=C["surface"])
            canvas.create_text(18, y, anchor="w", text=f"{value:.2f}",
                               fill=C["text_dim"], font=("Segoe UI", 9))

        canvas.create_line(left, top, left, bottom, fill=C["text_dim"], width=1)
        canvas.create_line(left, bottom, right, bottom, fill=C["text_dim"], width=1)

        for idx, item in enumerate(items):
            value = float(item.get("value", 0.0))
            x1 = left + gap + idx * (bar_w + gap)
            x2 = x1 + bar_w
            y1 = bottom - ((value / max_y) * (bottom - top))
            canvas.create_rectangle(x1, y1, x2, bottom, fill=color, outline="", width=0)
            canvas.create_text((x1 + x2) / 2, y1 - 10, text=f"{value:.2f}",
                               fill=C["text"], font=("Segoe UI", 9, "bold"))
            label = str(item.get("label", ""))[:24]
            canvas.create_text((x1 + x2) / 2, bottom + 18, text=label,
                               fill=C["text_dim"], font=("Segoe UI", 9), width=bar_w + 22)

    def _render_report_tabs(self, report_data: dict | None):
        self._report_data = report_data

        # ── helpers ──────────────────────────────────────────────────────────

        def _safe_width(canvas: tk.Canvas, fallback: int = 560) -> int:
            """Return the canvas's real pixel width, with a sensible fallback."""
            w = canvas.winfo_width()
            return w if w > 10 else fallback

        def _draw_charts_after_layout():
            """Draw all four charts once Tkinter has finished layout."""
            if not self._report_data:
                return
            rd = self._report_data

            w1 = _safe_width(self.current_loc_canvas)
            self.current_loc_canvas.config(width=w1)
            self._draw_bar_chart(
                self.current_loc_canvas,
                "Energy Consumption by LOC Range",
                rd["current"].get("energy_loc_bars", []),
                C["accent"],
            )

            w2 = _safe_width(self.current_hotspot_canvas)
            self.current_hotspot_canvas.config(width=w2)
            hs_items = [
                {"label": item["name"], "value": item["score"]}
                for item in rd["current"].get("hotspots", [])
            ]
            self._draw_bar_chart(
                self.current_hotspot_canvas,
                "Current Hotspots",
                hs_items,
                C["warn"],
            )

            w3 = _safe_width(self.energy_trend_canvas)
            self.energy_trend_canvas.config(width=w3)
            self._draw_line_chart(
                self.energy_trend_canvas,
                "Cumulative Energy vs Code Sample Number",
                rd["cumulative"].get("energy_trend", {}).get("points", []),
                C["accent"],
            )

            w4 = _safe_width(self.cumulative_loc_canvas)
            self.cumulative_loc_canvas.config(width=w4)
            self._draw_bar_chart(
                self.cumulative_loc_canvas,
                "Cumulative Energy by LOC Range",
                rd["cumulative"].get("loc_bucket_energy", []),
                C["accent3"],
            )

        # ── no data path ─────────────────────────────────────────────────────
        if not report_data:
            self._set_text_content(self.current_report_text, "Current report unavailable.")
            self._set_text_content(self.cumulative_report_text, "Cumulative report unavailable.")
            self._render_summary_panel(
                self.current_summary_frame, "Current report unavailable.", C["accent"])
            self._render_summary_panel(
                self.cumulative_summary_frame, "Cumulative report unavailable.", C["accent3"])
            self.after(50, lambda: (
                self._draw_placeholder(self.current_loc_canvas,
                    "Energy Consumption by LOC Range",
                    "Run an analysis to populate this report."),
                self._draw_placeholder(self.current_hotspot_canvas,
                    "Current Hotspots",
                    "Run an analysis to populate this report."),
                self._draw_placeholder(self.energy_trend_canvas,
                    "Cumulative Energy vs Code Sample Number",
                    "Run history will appear here."),
                self._draw_placeholder(self.cumulative_loc_canvas,
                    "Cumulative Energy by LOC Range",
                    "Run history will appear here."),
            ))
            return

        # ── data path ─────────────────────────────────────────────────────────
        self._set_text_content(self.current_report_text, report_data["current"]["summary"])
        self._set_text_content(self.cumulative_report_text, report_data["cumulative"]["summary"])
        self._render_summary_panel(
            self.current_summary_frame, report_data["current"]["summary"], C["accent"])
        self._render_summary_panel(
            self.cumulative_summary_frame, report_data["cumulative"]["summary"], C["accent3"])

        # Defer chart drawing so Tkinter finishes layout first
        self.after(80, _draw_charts_after_layout)

    def _classify_line(self, line: str) -> str:
        """Pick a colour tag based on content of an output line."""
        s = line.strip()
        if re.search(r"[═─]{5,}", s):
            return "header"
        if re.search(r"\[ERROR\]", s):
            return "error"
        if re.search(r"\[WARNING\]", s):
            return "warning"
        if re.search(r"\[LINT\]", s):
            return "info"
        if re.search(r"\[INFO\]", s):
            return "info"
        if re.search(r"✓.*clean|No syntax errors|no.*error", s, re.I):
            return "ok"
        if re.search(r"✗.*error|ERRORS FOUND", s, re.I):
            return "error"
        if re.search(r"How to fix|#\d+\s+", s):
            return "fix"
        if re.search(r"Error #\d|Error class|Error type|Message|Severity", s):
            return "title"
        if re.search(r"Source code\s*:", s):
            return "srcline"
        if re.search(r"^\s+\^\s*$", s):
            return "caret"
        if re.search(r"└──", s):
            return "error"
        if re.search(r"Explanation|Detailed Error", s):
            return "dim"
        return ""   # default colour

    # ── Carbon & Power panel ─────────────────────────────────────────────────

    def _render_carbon_panel(self, report_data: dict | None):
        """Draw the Carbon & Power dashboard inside self._carbon_inner."""
        frame = self._carbon_inner
        for w in frame.winfo_children():
            w.destroy()

        BG       = "#0f1117"
        CARD_BG  = "#161b22"
        BORDER   = "#30363d"
        GREEN    = "#3fb950"
        BLUE     = "#58a6ff"
        ORANGE   = "#d29922"
        RED      = "#ff7b72"
        DIM      = "#6e7681"
        WHITE    = "#e6edf3"

        def _card(parent, title: str, value: str, unit: str, color: str, note: str = ""):
            c = tk.Frame(parent, bg=CARD_BG,
                         highlightthickness=1, highlightbackground=BORDER)
            bar = tk.Frame(c, bg=color, height=4)
            bar.pack(fill="x", side="top")
            body = tk.Frame(c, bg=CARD_BG)
            body.pack(fill="both", expand=True, padx=14, pady=10)
            tk.Label(body, text=title.upper(), bg=CARD_BG, fg=DIM,
                     font=("Segoe UI", 8, "bold"), anchor="w").pack(anchor="w")
            tk.Label(body, text=value, bg=CARD_BG, fg=color,
                     font=("Consolas", 20, "bold"), anchor="w").pack(anchor="w", pady=(4, 0))
            tk.Label(body, text=unit, bg=CARD_BG, fg=DIM,
                     font=("Segoe UI", 8), anchor="w").pack(anchor="w")
            if note:
                tk.Label(body, text=note, bg=CARD_BG, fg=WHITE,
                         font=("Segoe UI", 8), anchor="w",
                         wraplength=260, justify="left").pack(anchor="w", pady=(6, 0))
            return c

        if not report_data:
            tk.Label(frame, text="Run an analysis to see Carbon & Power metrics.",
                     bg=BG, fg=DIM, font=("Segoe UI", 12)).pack(pady=60)
            return

        curr = report_data.get("current", {})
        cum  = report_data.get("cumulative", {})
        run  = report_data.get("run", {})

        power_mw      = curr.get("power_mw",      run.get("power_mw",      0.0))
        carbon_ug     = curr.get("carbon_ug_co2", run.get("carbon_ug_co2", 0.0))
        energy_mj     = run.get("estimated_energy_mj", 0.0)
        total_carbon  = cum.get("total_carbon_ug",  0.0)
        avg_power     = cum.get("avg_power_mw",     0.0)

        # Format helpers
        def _fmt_ug(ug: float) -> str:
            if ug < 1_000:
                return f"{ug:.4f}"
            if ug < 1_000_000:
                return f"{ug / 1_000:.4f}"
            return f"{ug / 1_000_000:.6f}"

        def _ug_unit(ug: float) -> str:
            if ug < 1_000:    return "µg CO₂"
            if ug < 1_000_000: return "mg CO₂"
            return "g CO₂"

        # Header
        hdr = tk.Frame(frame, bg="#0d1117", height=56)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="  🌱  Carbon Emission & Power Consumption",
                 bg="#0d1117", fg=GREEN,
                 font=("Segoe UI", 14, "bold")).pack(side="left", padx=16, pady=12)
        tk.Label(hdr, text="Based on global avg grid intensity: 233 g CO₂ / kWh",
                 bg="#0d1117", fg=DIM,
                 font=("Segoe UI", 8)).pack(side="right", padx=16, pady=12)

        # Card grid — row 1
        row1 = tk.Frame(frame, bg=BG)
        row1.pack(fill="x", padx=14, pady=(12, 6))
        for col in range(3):
            row1.grid_columnconfigure(col, weight=1)

        _card(row1,
              "Power Draw (this run)",
              f"{power_mw:.4f}", "milliwatts (mW)",
              BLUE).grid(row=0, column=0, sticky="nsew", padx=6, pady=6)

        _card(row1,
              "Carbon Emission (this run)",
              _fmt_ug(carbon_ug), _ug_unit(carbon_ug),
              GREEN).grid(row=0, column=1, sticky="nsew", padx=6, pady=6)

        _card(row1,
              "Energy Consumed (this run)",
              f"{energy_mj:.4f}", "millijoules (mJ)",
              ORANGE).grid(row=0, column=2, sticky="nsew", padx=6, pady=6)

        # Card grid — row 2 (cumulative)
        row2 = tk.Frame(frame, bg=BG)
        row2.pack(fill="x", padx=14, pady=(0, 6))
        for col in range(2):
            row2.grid_columnconfigure(col, weight=1)

        _card(row2,
              "Cumulative Carbon (all runs)",
              _fmt_ug(total_carbon), _ug_unit(total_carbon),
              RED).grid(row=0, column=0, sticky="nsew", padx=6, pady=6)

        _card(row2,
              "Avg Power Draw (all runs)",
              f"{avg_power:.4f}", "milliwatts (mW)",
              BLUE).grid(row=0, column=1, sticky="nsew", padx=6, pady=6)

        # Equivalence context
        ctx_frame = tk.Frame(frame, bg=CARD_BG,
                             highlightthickness=1, highlightbackground=BORDER)
        ctx_frame.pack(fill="x", padx=20, pady=(4, 10))
        tk.Frame(ctx_frame, bg=GREEN, height=4).pack(fill="x", side="top")
        ctx_body = tk.Frame(ctx_frame, bg=CARD_BG)
        ctx_body.pack(fill="x", padx=16, pady=12)
        tk.Label(ctx_body, text="EQUIVALENCE CONTEXT",
                 bg=CARD_BG, fg=DIM,
                 font=("Segoe UI", 8, "bold"), anchor="w").pack(anchor="w")

        # LED equivalent
        led_ug_per_sec = (233_000 / 3_600_000) * 5.0 * 1000 / 3600
        led_s = carbon_ug / led_ug_per_sec if led_ug_per_sec > 0 else 0
        runs_per_gram = (1_000_000 / carbon_ug) if carbon_ug > 0 else 0

        ctx_lines = [
            f"• This analysis emitted ≈ {_fmt_ug(carbon_ug)} {_ug_unit(carbon_ug)} CO₂.",
            f"• Equivalent to running a 5 W LED for ≈ {led_s:.4f} seconds.",
        ]
        if runs_per_gram >= 1:
            ctx_lines.append(f"• ≈ {runs_per_gram:,.0f} such analyses would emit 1 gram of CO₂.")
        ctx_lines.append(f"• Cumulative carbon across all {report_data.get('run', {}).get('run_number', '?')} run(s): {_fmt_ug(total_carbon)} {_ug_unit(total_carbon)} CO₂.")

        for line in ctx_lines:
            tk.Label(ctx_body, text=line,
                     bg=CARD_BG, fg=WHITE,
                     font=("Segoe UI", 10), anchor="w",
                     justify="left", wraplength=900).pack(anchor="w", pady=2)

        # Tips
        tips_frame = tk.Frame(frame, bg="#0d1117",
                              highlightthickness=1, highlightbackground=BORDER)
        tips_frame.pack(fill="x", padx=20, pady=(0, 14))
        tk.Frame(tips_frame, bg=ORANGE, height=4).pack(fill="x", side="top")
        tips_body = tk.Frame(tips_frame, bg="#0d1117")
        tips_body.pack(fill="x", padx=16, pady=12)
        tk.Label(tips_body, text="💡  GREEN CODING TIPS",
                 bg="#0d1117", fg=ORANGE,
                 font=("Segoe UI", 9, "bold"), anchor="w").pack(anchor="w")
        tips = [
            "• Reduce cyclomatic complexity — fewer branches = less CPU work.",
            "• Avoid deeply nested loops over large datasets.",
            "• Prefer built-in functions (implemented in C) over pure-Python equivalents.",
            "• Remove dead code and unreachable branches to reduce parse/IR overhead.",
            "• Use generators instead of building full lists when streaming data.",
        ]
        for tip in tips:
            tk.Label(tips_body, text=tip,
                     bg="#0d1117", fg=DIM,
                     font=("Segoe UI", 9), anchor="w",
                     justify="left").pack(anchor="w", pady=1)

    # ── Execution mode ───────────────────────────────────────────────────────

    def _show_input_dialog(self, n_inputs: int) -> list[str] | None:
        """
        Open a dialog that prompts the user to enter values for each input() call.
        Returns a list of strings (one per detected input call), or None if cancelled.
        """
        dialog = tk.Toplevel(self)
        dialog.title("Program Input Required")
        dialog.configure(bg=C["bg"])
        dialog.resizable(False, False)
        dialog.grab_set()  # modal

        # Header
        hdr = tk.Frame(dialog, bg=C["accent"], height=48)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(
            hdr, text="⌨  Program Input Required",
            bg=C["accent"], fg="#ffffff",
            font=("Segoe UI", 13, "bold"),
        ).pack(side="left", padx=16, pady=10)

        body = tk.Frame(dialog, bg=C["bg"])
        body.pack(fill="both", padx=20, pady=16)

        tk.Label(
            body,
            text=f"This program calls input() {n_inputs} time(s).\n"
                  "Enter each value below (one per line in the order they will be requested).",
            bg=C["bg"], fg=C["text"],
            font=("Segoe UI", 10),
            justify="left",
        ).pack(anchor="w", pady=(0, 12))

        # Multi-line entry for all inputs
        tk.Label(
            body, text="Input values (one per line):",
            bg=C["bg"], fg=C["text_dim"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")

        entry_frame = tk.Frame(body, bg=C["surface"], highlightthickness=1,
                               highlightbackground=C["surface"])
        entry_frame.pack(fill="x", pady=(4, 16))

        input_text = tk.Text(
            entry_frame, height=max(n_inputs, 3), width=52,
            font=("Consolas", 11), bg=C["bg3"], fg=C["text"],
            relief="flat", padx=8, pady=6,
            insertbackground=C["accent"],
        )
        input_text.pack(fill="x")
        input_text.focus_set()

        result_holder: list = [None]

        def _ok():
            raw = input_text.get("1.0", "end-1c")
            # Split by newlines; pad/trim to match n_inputs
            vals = raw.splitlines()
            # Pad with empty strings if the user gave fewer than expected
            while len(vals) < n_inputs:
                vals.append("")
            result_holder[0] = vals
            dialog.destroy()

        def _cancel():
            result_holder[0] = None
            dialog.destroy()

        btn_row = tk.Frame(body, bg=C["bg"])
        btn_row.pack(fill="x")
        HoverButton(
            btn_row, text="▶  Run Program",
            hover_bg=C["btn_hover"], normal_bg=C["btn_bg"],
            fg=C["btn_fg"], font=("Segoe UI", 10, "bold"),
            command=_ok, padx=16, pady=6,
        ).pack(side="left")
        HoverButton(
            btn_row, text="Cancel",
            hover_bg=C["btn2_hover"], normal_bg=C["btn2_bg"],
            fg=C["btn2_fg"], font=("Segoe UI", 10),
            command=_cancel, padx=16, pady=6,
        ).pack(side="left", padx=8)

        # Escape cancels; Enter types a newline in the text box (normal behaviour).
        # Ctrl+Enter is provided as a keyboard shortcut to submit.
        dialog.bind("<Escape>", lambda _: _cancel())
        input_text.bind("<Control-Return>", lambda _: _ok())

        # Center the dialog over the main window
        self.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width()  - dialog.winfo_reqwidth())  // 2
        y = self.winfo_rooty() + (self.winfo_height() - dialog.winfo_reqheight()) // 2
        dialog.geometry(f"+{x}+{y}")

        self.wait_window(dialog)
        return result_holder[0]

    def _run_code(self):
        """Execute the last successfully-analyzed source code."""
        if not self._can_run or not self._last_source:
            messagebox.showwarning(
                "Cannot Run",
                "Please analyze the code first and ensure there are no errors."
            )
            return

        source = self._last_source
        heal_note = ""   # message shown in Execution tab if we auto-repaired

        # ── Pre-execution syntax check & auto-heal ────────────────────────
        # Our custom parser may have cleared errors during analysis, but Python's
        # own compiler may still see syntax problems (e.g. missing ':').
        # Run the healer iteratively until compile() passes or we give up.
        try:
            compile(source, "<editor>", "exec")
        except SyntaxError:
            try:
                from self_heal import heal_source as _heal
                from lexers import tokenize_python
                from parsers import parse_python

                working = source
                for _pass in range(8):
                    try:
                        compile(working, "<editor>", "exec")
                        break          # clean — stop
                    except SyntaxError:
                        pass

                    errors = []
                    try:
                        _, errors = parse_python(tokenize_python(working))
                    except Exception:
                        pass

                    if not errors:
                        # Parser sees no errors but compile() still fails —
                        # likely a construct our parser misses; use Python's
                        # own error to guide the fix.
                        try:
                            compile(working, "<editor>", "exec")
                        except SyntaxError as se:
                            # Build a minimal error stub for the healer
                            from types import SimpleNamespace
                            stub = SimpleNamespace(
                                error_type="MISSING_COLON",
                                message=str(se.msg),
                                line=se.lineno or 1,
                                column=se.offset or 1,
                                token=None,
                            )
                            errors = [stub]

                    result = _heal(working, errors, language="python",
                                   defined_names=set())
                    if result.healed_source and result.healed_source != working:
                        working = result.healed_source
                    else:
                        break   # healer made no progress

                # Final check
                try:
                    compile(working, "<editor>", "exec")
                    source = working
                    heal_note = (
                        "⚙  Auto-repaired syntax before execution "
                        "(e.g. added missing ':').\n"
                        "   Consider fixing your source code to match.\n"
                    )
                except SyntaxError as se:
                    # Healer couldn't fully fix it — still try with best effort
                    source = working
                    heal_note = (
                        f"⚠  Partial auto-repair applied; Python may still "
                        f"report errors (line {se.lineno}: {se.msg}).\n"
                    )
            except Exception:
                pass    # If anything goes wrong, just run original source

        # Detect input() calls
        n_inputs = detect_input_calls(source)
        user_inputs: list[str] = []

        if n_inputs > 0:
            user_inputs_or_none = self._show_input_dialog(n_inputs)
            if user_inputs_or_none is None:
                return  # user cancelled
            user_inputs = user_inputs_or_none

        # Switch to Execution tab
        self._notebook.select(7)

        # Show running indicator
        self.exec_view.config(state="normal")
        self.exec_view.delete("1.0", "end")
        sep = "═" * 64 + "\n"
        self.exec_view.insert("end", sep, "exec_sep")
        self.exec_view.insert("end", "  ▶  Program Execution\n", "exec_header")
        self.exec_view.insert("end", sep, "exec_sep")
        if heal_note:
            self.exec_view.insert("end", f"\n  {heal_note}\n", "exec_input")
        if user_inputs:
            self.exec_view.insert("end", "\n  📥 Provided Inputs:\n", "exec_input")
            for i, val in enumerate(user_inputs, 1):
                display_val = val if val else "(empty)"
                self.exec_view.insert("end", f"     [{i}] {display_val}\n", "exec_input")
        self.exec_view.insert("end", "\n  ⏳ Running…\n", "exec_dim")
        self.exec_view.config(state="disabled")
        self._exec_status_label.config(text="Running…", fg=C["warn"])
        self._run_btn.config(state="disabled", text="⏳  Running…")
        self.update_idletasks()

        def _worker():
            stdout, stderr, returncode = run_code(source, user_inputs)
            self.after(0, lambda: self._display_execution(stdout, stderr, returncode, user_inputs))

        threading.Thread(target=_worker, daemon=True).start()

    def _display_execution(self, stdout: str, stderr: str, returncode: int, user_inputs: list[str]):
        """Render execution results in the Execution tab."""
        self._run_btn.config(state="normal", text="▶▶  Run Code", bg="#16a34a")

        self.exec_view.config(state="normal")
        self.exec_view.delete("1.0", "end")

        sep = "═" * 64 + "\n"
        thin_sep = "─" * 64 + "\n"

        self.exec_view.insert("end", sep, "exec_sep")
        self.exec_view.insert("end", "  ▶  Program Execution\n", "exec_header")
        self.exec_view.insert("end", sep, "exec_sep")

        # Provided inputs section
        if user_inputs:
            self.exec_view.insert("end", "\n  📥 Provided Inputs:\n", "exec_input")
            for i, val in enumerate(user_inputs, 1):
                display_val = val if val else "(empty)"
                self.exec_view.insert("end", f"     [{i}] {display_val}\n", "exec_input")
            self.exec_view.insert("end", "\n", "")

        # Stdout section
        self.exec_view.insert("end", thin_sep, "exec_sep")
        self.exec_view.insert("end", "  📤 Output:\n", "exec_header")
        self.exec_view.insert("end", thin_sep, "exec_sep")
        if stdout.strip():
            for line in stdout.splitlines(keepends=True):
                self.exec_view.insert("end", "  " + line, "exec_stdout")
        else:
            self.exec_view.insert("end", "  (no output)\n", "exec_dim")

        # Stderr section (only if there's something)
        if stderr.strip():
            self.exec_view.insert("end", "\n" + thin_sep, "exec_sep")
            self.exec_view.insert("end", "  ⚠  Stderr / Traceback:\n", "exec_stderr")
            self.exec_view.insert("end", thin_sep, "exec_sep")
            for line in stderr.splitlines(keepends=True):
                self.exec_view.insert("end", "  " + line, "exec_stderr")

        # Exit status
        self.exec_view.insert("end", "\n" + sep, "exec_sep")
        if returncode == 0:
            self.exec_view.insert("end", "  ✓  Process exited successfully (code 0)\n", "exec_ok")
            self._exec_status_label.config(text="Exit code 0  ✓", fg="#15803d")
        else:
            self.exec_view.insert("end", f"  ✗  Process exited with code {returncode}\n", "exec_fail")
            self._exec_status_label.config(text=f"Exit code {returncode}  ✗", fg=C["error"])
        self.exec_view.insert("end", sep, "exec_sep")
        self.exec_view.config(state="disabled")
        self.exec_view.see("1.0")

    # ── Clipboard / save ─────────────────────────────────────────────────────

    def _copy_results(self):
        # Copy whichever tab is currently visible
        active = self._notebook.index(self._notebook.select())
        tab_map = {
            0: ("Diagnostics", self.results),
            1: ("AST", self.ast_view),
            2: ("IR", self.ir_view),
            3: ("Security report", self.security_view),
            4: ("Current report", self.current_report_text),
            5: ("Cumulative report", self.cumulative_report_text),
            7: ("Execution output", self.exec_view),
        }
        label, widget = tab_map.get(active, ("Report", self.results))
        text = widget.get("1.0", "end-1c")
        if text.strip():
            self.clipboard_clear()
            self.clipboard_append(text)
            self._status_text.set(f"{label} report copied to clipboard.")
        else:
            messagebox.showinfo("Nothing to copy", "Run the analysis first.")

    def _save_report(self):
        active = self._notebook.index(self._notebook.select())
        tab_map = {
            0: ("diagnostics", self.results),
            1: ("ast", self.ast_view),
            2: ("ir", self.ir_view),
            3: ("security_report", self.security_view),
            4: ("current_report", self.current_report_text),
            5: ("cumulative_report", self.cumulative_report_text),
            7: ("execution_output", self.exec_view),
        }
        label, widget = tab_map.get(active, ("diagnostics", self.results))
        text = widget.get("1.0", "end-1c")
        if not text.strip():
            messagebox.showinfo("Nothing to save", "Run the analysis first.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=f"report_{label}.txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save report",
        )
        if path:
            try:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(text)
                self._status_text.set(f"Report saved: {os.path.basename(path)}")
            except Exception as exc:
                messagebox.showerror("Save Error", str(exc))


# ════════════════════════════════════════════════════════════════════════════
# Entry point
# ════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = SyntaxAnalyzerGUI()
    app.mainloop()
