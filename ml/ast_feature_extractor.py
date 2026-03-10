"""
AST-Based Feature Extractor
============================
Extracts six groups of features from each parse error:

  1. Error metadata      – error_type, message, token (text → TF-IDF)
  2. Token window        – ±5 tokens around the error line (text → TF-IDF)
  3. AST path            – root-to-error path string  (text → TF-IDF)
  4. Nearby keywords     – keyword tokens in window   (text → TF-IDF)
  5. Structural numeric  – function/loop/if counts, max depth, LOC, etc.
  6. Error co-occurrence – which OTHER error types appear in the same file

Feature groups 1-4 are concatenated into one text string for TF-IDF.
Feature groups 5-6 are numeric vectors scaled separately.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from syntax_tree.ast_nodes import (
    ASTNode, Program, FunctionDecl, ClassDecl,
    IfStmt, WhileStmt, ForStmt, ErrorNode,
)

# ── Unsafe pattern label mapping ──────────────────────────────────────────────

# Maps the fragment extracted from a dataset filename to a pattern class.
LABEL_MAP: Dict[str, str] = {
    'missing_colon':        'UNSAFE_BLOCK_SCOPE',
    'missing_paren':        'UNSAFE_EXPRESSION_BOUNDARY',
    'missing_bracket':      'UNSAFE_EXPRESSION_BOUNDARY',
    'missing_brace':        'UNSAFE_EXPRESSION_BOUNDARY',
    'indentation_error':    'UNSAFE_SCOPE_LEAK',
    'incomplete_statement': 'UNSAFE_INCOMPLETE_OPERATION',
    'invalid_syntax':       'UNSAFE_UNDEFINED_BEHAVIOR',
}

# Ordered unique class list — needed for partial_fit and calibration.
ALL_LABELS: List[str] = list(dict.fromkeys(LABEL_MAP.values()))

# Heuristic base severity scores per pattern (used by the severity regressor
# as hard-coded targets when no human-annotated labels exist).
SEVERITY_BASE: Dict[str, float] = {
    'UNSAFE_BLOCK_SCOPE':          8.0,
    'UNSAFE_EXPRESSION_BOUNDARY':  7.0,
    'UNSAFE_SCOPE_LEAK':           9.0,
    'UNSAFE_INCOMPLETE_OPERATION': 6.0,
    'UNSAFE_UNDEFINED_BEHAVIOR':   7.5,
}

# All known error type tokens — used for the co-occurrence binary vector.
ALL_ERROR_TYPES: List[str] = [
    'MISSING_COLON', 'MISSING_PAREN', 'MISSING_BRACKET', 'MISSING_BRACE',
    'INDENTATION_ERROR', 'INCONSISTENT_INDENTATION', 'INCOMPLETE_STATEMENT',
    'INVALID_SYNTAX', 'INVALID_EXPRESSION', 'KEYWORD_MISUSE',
    'UNMATCHED_DELIMITER', 'INVALID_IMPORT', 'INVALID_FUNCTION_DEF',
    'INVALID_CLASS_DEF', 'UNEXPECTED_EOF', 'INVALID_DECORATOR',
    'SyntaxError', 'UnexpectedEOF', 'MAX_ERRORS_EXCEEDED',
]

_ERROR_TYPE_INDEX: Dict[str, int] = {e: i for i, e in enumerate(ALL_ERROR_TYPES)}


# ── Feature container ─────────────────────────────────────────────────────────

@dataclass
class ErrorFeatures:
    """
    All features for a single ErrorNode, ready for the sklearn pipeline.

    Text fields are later concatenated by _TextExtractor and fed into TF-IDF.
    Numeric fields are stacked by _NumericExtractor and scaled with StandardScaler.
    """

    # ── Text features (→ TF-IDF) ──────────────────────────────────────────
    error_type:      str = ""   # e.g. MISSING_COLON
    error_message:   str = ""   # raw parser message
    error_token:     str = ""   # offending token value
    token_window:    str = ""   # "TYPE:value TYPE:value …" ±5 tokens
    nearby_keywords: str = ""   # keyword values within the window
    ast_path:        str = ""   # "Program>FunctionDecl>IfStmt>[ERROR]"

    # ── Structural numeric features ───────────────────────────────────────
    num_functions:      int = 0
    num_if_stmts:       int = 0
    num_loops:          int = 0
    max_nesting_depth:  int = 0
    total_statements:   int = 0
    errors_total:       int = 0
    total_tokens:       int = 0
    keyword_density:    float = 0.0   # keywords / total_tokens
    delimiter_imbalance: int = 0      # abs(open delimiters - close delimiters)

    # ── Error-location context ────────────────────────────────────────────
    error_nesting_depth:    int = 0
    error_inside_function:  int = 0   # boolean as 0/1
    error_inside_loop:      int = 0   # boolean as 0/1
    has_try_keyword_nearby: int = 0   # boolean as 0/1

    # ── Error co-occurrence vector ────────────────────────────────────────
    # Binary vector of length len(ALL_ERROR_TYPES):
    # co_occurrence[i] = 1 if error type i also appears in this file's errors
    co_occurrence: List[int] = field(default_factory=lambda: [0] * len(ALL_ERROR_TYPES))

    # ── Ground truth (filled when building training data) ─────────────────
    label:          str   = ""
    severity_score: float = 0.0   # 0–10


# ── Extractor ─────────────────────────────────────────────────────────────────

class ASTFeatureExtractor:
    """
    Extracts all ML features for a list of ErrorNodes produced by the parser.

    Usage:
        extractor = ASTFeatureExtractor(tokens, ast_program)
        features  = extractor.extract(errors, label="missing_colon")
    """

    _FUNCTION_NODES = frozenset({'FunctionDecl'})
    _LOOP_NODES     = frozenset({'WhileStmt', 'ForStmt'})
    _IF_NODES       = frozenset({'IfStmt'})

    def __init__(self, tokens: list, ast_program: Program):
        self.tokens      = tokens
        self.ast_program = ast_program
        self._struct     = self._analyse_structure()
        self._tok_stats  = self._analyse_tokens()

    # ── Public API ────────────────────────────────────────────────────────

    def extract(self,
                errors: List[ErrorNode],
                label:  str = "") -> List[ErrorFeatures]:
        """Return one ErrorFeatures per ErrorNode."""
        severity_base = SEVERITY_BASE.get(LABEL_MAP.get(label, ""), 5.0)
        co_vec        = self._build_co_occurrence(errors)

        results = []
        for err in errors:
            feat = ErrorFeatures(
                label          = LABEL_MAP.get(label, label),
                severity_score = severity_base,
                errors_total   = len(errors),
                co_occurrence  = list(co_vec),
            )
            self._fill_struct(feat)
            self._fill_tok_stats(feat)
            self._fill_error_meta(feat, err)
            self._fill_token_window(feat, err)
            self._fill_ast_path(feat, err)
            self._fill_error_context(feat, err)
            results.append(feat)

        return results

    # ── Structural AST walk ───────────────────────────────────────────────

    def _analyse_structure(self) -> Dict[str, int]:
        stats: Dict[str, int] = {
            'num_functions':     0,
            'num_if_stmts':      0,
            'num_loops':         0,
            'max_nesting_depth': 0,
            'total_statements':  0,
        }
        self._walk(self.ast_program, depth=0, stats=stats)
        return stats

    def _walk(self, node: Any, depth: int, stats: Dict[str, int]) -> None:
        if not isinstance(node, ASTNode):
            return

        name = node.__class__.__name__
        stats['max_nesting_depth'] = max(stats['max_nesting_depth'], depth)

        if name in self._FUNCTION_NODES:
            stats['num_functions'] += 1
            stats['total_statements'] += 1
        elif name in self._LOOP_NODES:
            stats['num_loops'] += 1
            stats['total_statements'] += 1
        elif name in self._IF_NODES:
            stats['num_if_stmts'] += 1
            stats['total_statements'] += 1
        elif name not in ('Program', 'Block'):
            stats['total_statements'] += 1

        for val in node.__dict__.values():
            if isinstance(val, ASTNode):
                self._walk(val, depth + 1, stats)
            elif isinstance(val, list):
                for item in val:
                    if isinstance(item, ASTNode):
                        self._walk(item, depth + 1, stats)

    def _fill_struct(self, feat: ErrorFeatures) -> None:
        feat.num_functions     = self._struct['num_functions']
        feat.num_if_stmts      = self._struct['num_if_stmts']
        feat.num_loops         = self._struct['num_loops']
        feat.max_nesting_depth = self._struct['max_nesting_depth']
        feat.total_statements  = self._struct['total_statements']

    # ── Token-level statistics ────────────────────────────────────────────

    def _analyse_tokens(self) -> Dict[str, Any]:
        total    = len(self.tokens)
        keywords = sum(1 for t in self.tokens if t.type == 'KEYWORD')
        opens    = sum(1 for t in self.tokens
                       if t.type == 'DELIMITER' and t.value in '([{')
        closes   = sum(1 for t in self.tokens
                       if t.type == 'DELIMITER' and t.value in ')]}')
        return {
            'total_tokens':       total,
            'keyword_density':    round(keywords / max(total, 1), 4),
            'delimiter_imbalance': abs(opens - closes),
        }

    def _fill_tok_stats(self, feat: ErrorFeatures) -> None:
        feat.total_tokens       = self._tok_stats['total_tokens']
        feat.keyword_density    = self._tok_stats['keyword_density']
        feat.delimiter_imbalance = self._tok_stats['delimiter_imbalance']

    # ── Error metadata ────────────────────────────────────────────────────

    def _fill_error_meta(self, feat: ErrorFeatures, err: ErrorNode) -> None:
        feat.error_type    = err.error_type or ""
        feat.error_message = err.message    or ""
        feat.error_token   = err.token      or ""

    # ── Token window (Feature 2) ──────────────────────────────────────────

    def _fill_token_window(self, feat: ErrorFeatures, err: ErrorNode,
                           window: int = 5) -> None:
        idx  = self._token_idx_for_line(err.line)
        low  = max(0, idx - window)
        high = min(len(self.tokens), idx + window + 1)

        parts, kw_parts = [], []
        for tok in self.tokens[low:high]:
            parts.append(f"{tok.type}:{tok.value}")
            if tok.type == 'KEYWORD':
                kw_parts.append(tok.value)

        feat.token_window    = " ".join(parts)
        feat.nearby_keywords = " ".join(kw_parts)

        # Scan ±10 tokens for 'try' keyword
        lo2 = max(0, idx - 10)
        hi2 = min(len(self.tokens), idx + 10 + 1)
        feat.has_try_keyword_nearby = int(
            any(t.type == 'KEYWORD' and t.value == 'try'
                for t in self.tokens[lo2:hi2])
        )

    def _token_idx_for_line(self, target_line: int) -> int:
        for i, tok in enumerate(self.tokens):
            if tok.line >= target_line:
                return i
        return max(0, len(self.tokens) - 1)

    # ── AST path feature (Feature 3) ─────────────────────────────────────

    def _fill_ast_path(self, feat: ErrorFeatures, err: ErrorNode) -> None:
        path = self._find_path(self.ast_program, err.line)
        feat.ast_path = ">".join(path) if path else "Program>[ERROR]"

    def _find_path(self, node: Any, target_line: int,
                   path: Optional[List[str]] = None) -> Optional[List[str]]:
        if not isinstance(node, ASTNode):
            return None

        if path is None:
            path = []

        current_path = path + [node.__class__.__name__]
        node_line    = getattr(node, 'line', -1)

        if node_line > 0 and abs(node_line - target_line) <= 2:
            return current_path + ['[ERROR]']

        for val in node.__dict__.values():
            children: List[ASTNode] = []
            if isinstance(val, ASTNode):
                children = [val]
            elif isinstance(val, list):
                children = [v for v in val if isinstance(v, ASTNode)]

            for child in children:
                result = self._find_path(child, target_line, current_path)
                if result is not None:
                    return result

        return None

    # ── Error-location context ────────────────────────────────────────────

    def _fill_error_context(self, feat: ErrorFeatures, err: ErrorNode) -> None:
        result = self._find_context(
            self.ast_program, err.line,
            depth=0, in_func=False, in_loop=False
        )
        if result is not None:
            depth, in_func, in_loop = result
            feat.error_nesting_depth   = depth
            feat.error_inside_function = int(in_func)
            feat.error_inside_loop     = int(in_loop)

    def _find_context(self, node: Any, target_line: int,
                      depth: int, in_func: bool,
                      in_loop: bool) -> Optional[Tuple[int, bool, bool]]:
        if not isinstance(node, ASTNode):
            return None

        name    = node.__class__.__name__
        in_func = in_func or (name in self._FUNCTION_NODES)
        in_loop = in_loop or (name in self._LOOP_NODES)
        line    = getattr(node, 'line', -1)

        if line > 0 and abs(line - target_line) <= 2:
            return (depth, in_func, in_loop)

        for val in node.__dict__.values():
            children: List[ASTNode] = []
            if isinstance(val, ASTNode):
                children = [val]
            elif isinstance(val, list):
                children = [v for v in val if isinstance(v, ASTNode)]

            for child in children:
                res = self._find_context(child, target_line,
                                          depth + 1, in_func, in_loop)
                if res is not None:
                    return res

        return None

    # ── Error co-occurrence vector (Feature 6) ────────────────────────────

    def _build_co_occurrence(self, errors: List[ErrorNode]) -> List[int]:
        """Binary vector: which error types appear anywhere in the file."""
        vec = [0] * len(ALL_ERROR_TYPES)
        for err in errors:
            idx = _ERROR_TYPE_INDEX.get(err.error_type, -1)
            if idx >= 0:
                vec[idx] = 1
        return vec
