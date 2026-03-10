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
import sys
import threading
import tkinter as tk
from tkinter import filedialog, font, messagebox, scrolledtext, ttk

# ── Make sure the project root is importable ────────────────────────────────
_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

# ── Colour palette (VS Code – inspired dark theme) ──────────────────────────
C = {
    "bg":          "#1e1e2e",   # main background
    "bg2":         "#181825",   # sidebar / panels
    "bg3":         "#313244",   # input editor bg
    "surface":     "#45475a",   # separator / subtle elements
    "accent":      "#89b4fa",   # blue accent
    "accent2":     "#cba6f7",   # purple accent
    "accent3":     "#a6e3a1",   # green (clean)
    "error":       "#f38ba8",   # red (errors)
    "warn":        "#fab387",   # orange (warnings)
    "info":        "#89dceb",   # cyan (info)
    "text":        "#cdd6f4",   # main text
    "text_dim":    "#7f849c",   # dimmed text
    "lineno":      "#45475a",   # line number gutter bg
    "status_ok":   "#a6e3a1",
    "status_err":  "#f38ba8",
    "btn_bg":      "#89b4fa",
    "btn_fg":      "#1e1e2e",
    "btn_hover":   "#74c7ec",
    "btn2_bg":     "#313244",
    "btn2_fg":     "#cdd6f4",
    "btn2_hover":  "#45475a",
    "tab_active":  "#313244",
    "tab_inactive":"#181825",
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



def _build_ir_view(source: str) -> list:
    """
    Build the IR from source and return a list of (text, tag) chunks
    for display in the IR View tab.
    """
    lines = []

    def _add(text, tag=""):
        lines.append((text, tag))

    try:
        from lexers import tokenize_python
        from parsers import parse_python
        from ir import build_ir

        tokens = tokenize_python(source)
        ast_tree, _ = parse_python(tokens)
        ir_program = build_ir(ast_tree)

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
            analyse_python(source, filepath="<editor>")
        elif language in ("c", "java"):
            from analyze_code import analyse_parser_only
            analyse_parser_only(source, filepath="<editor>", language=language)
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

        self._setup_styles()
        self._build_ui()
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
        def _worker():
            output    = run_analysis(source, "python")
            ast_root  = build_ast(source, "python")
            ast_lines = render_ast_tree(ast_root, "python")
            ir_lines  = _build_ir_view(source)
            self.after(0, lambda: self._display_results(output, ast_lines, ir_lines))

        threading.Thread(target=_worker, daemon=True).start()

    def _display_results(self, output: str, ast_lines: list, ir_lines: list):
        """Called on the main thread after analysis completes."""
        self._progress.stop()
        self._progress.pack_forget()
        self._analyze_btn.config(state="normal", text="▶  Analyze Code")
        self._busy = False

        n_errors = count_errors(output)

        if n_errors == 0:
            self._status_label.config(fg=C["status_ok"])
            self._status_text.set("✓  Analysis complete — No errors found!")
            self._error_count_label.config(
                text="✓  Clean", fg=C["status_ok"])
        else:
            self._status_label.config(fg=C["status_err"])
            self._status_text.set(f"✗  Analysis complete — {n_errors} error(s) detected.")
            self._error_count_label.config(
                text=f"✗  {n_errors} Error{'s' if n_errors != 1 else ''}",
                fg=C["status_err"],
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

    def _classify_line(self, line: str) -> str:
        """Pick a colour tag based on content of an output line."""
        s = line.strip()
        if re.search(r"[═─]{5,}", s):
            return "header"
        if re.search(r"\[ERROR\]", s):
            return "error"
        if re.search(r"\[WARNING\]", s):
            return "warning"
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

    # ── Clipboard / save ─────────────────────────────────────────────────────

    def _copy_results(self):
        # Copy whichever tab is currently visible
        active = self._notebook.index(self._notebook.select())
        text = (self.results if active == 0 else self.ast_view).get("1.0", "end-1c")
        if text.strip():
            self.clipboard_clear()
            self.clipboard_append(text)
            label = "Diagnostics" if active == 0 else "AST"
            self._status_text.set(f"{label} report copied to clipboard.")
        else:
            messagebox.showinfo("Nothing to copy", "Run the analysis first.")

    def _save_report(self):
        active = self._notebook.index(self._notebook.select())
        text = (self.results if active == 0 else self.ast_view).get("1.0", "end-1c")
        if not text.strip():
            messagebox.showinfo("Nothing to save", "Run the analysis first.")
            return
        label = "diagnostics" if active == 0 else "ast"
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
