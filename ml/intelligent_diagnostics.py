"""
Intelligent Diagnostics Engine
================================
Loads all trained ML models and, given Python source code, produces a
structured DiagnosticReport containing:

  • Unsafe pattern classification   (calibrated probability)
  • Risk severity score             (0 – 10, from Ridge regressor)
  • Top-3 ranked specific fix actions
  • Anomaly flag for valid-looking but structurally suspicious code
  • Human-readable summary

Usage:
    engine = IntelligentDiagnosticsEngine()
    report = engine.analyse_source(source_code)
    print(report.summary())
    data   = report.to_dict()   # JSON-serialisable
"""

from __future__ import annotations

import os
import pickle
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import numpy as np

from lexers import tokenize_python
from parsers import parse_python
# Import custom sklearn transformers so pickle can resolve them when loading models
from ml.train_classifier import _TextExtractor, _NumericExtractor  # noqa: F401
from ml.ast_feature_extractor import (
    ASTFeatureExtractor, ErrorFeatures,
    ALL_LABELS,
)
from ml.train_classifier import (
    _NumericExtractor, FIX_ACTIONS,
)

# ── Pattern knowledge base ────────────────────────────────────────────────────

_PATTERNS: Dict[str, Dict[str, str]] = {

    'UNSAFE_BLOCK_SCOPE': {
        'severity_label': 'ERROR',
        'title':     'Missing Block Header — Scope Corruption Risk',
        'why_unsafe': (
            "A missing colon after if/for/while/def/class leaves the block "
            "header malformed. Code meant to be conditional or scoped may "
            "execute unconditionally at the outer level, silently bypassing "
            "guards and invariants."
        ),
    },

    'UNSAFE_EXPRESSION_BOUNDARY': {
        'severity_label': 'ERROR',
        'title':     'Unmatched Delimiter — Expression Grouping Error',
        'why_unsafe': (
            "An unmatched '(', '[', or '{' extends the expression beyond its "
            "intended boundary, silently changing operator precedence and "
            "applying operations to unintended operands."
        ),
    },

    'UNSAFE_SCOPE_LEAK': {
        'severity_label': 'ERROR',
        'title':     'Indentation Error — Code Executes in Wrong Scope',
        'why_unsafe': (
            "Python uses indentation to define scope. A wrong indent level "
            "re-assigns a block to the wrong parent statement. Code meant to "
            "run inside a loop or function may leak to the outer scope and "
            "execute unconditionally — or outer code becomes unreachable."
        ),
    },

    'UNSAFE_INCOMPLETE_OPERATION': {
        'severity_label': 'WARNING',
        'title':     'Incomplete Statement — Uninitialized Variable Risk',
        'why_unsafe': (
            "A partial statement (e.g., 'x =' with no RHS) leaves a variable "
            "uninitialized or an expression unevaluated. Accessing the result "
            "later raises NameError or produces incorrect values without any "
            "explicit crash at the problem site."
        ),
    },

    'UNSAFE_UNDEFINED_BEHAVIOR': {
        'severity_label': 'WARNING',
        'title':     'Invalid Syntax — Execution Path Unpredictable',
        'why_unsafe': (
            "The parser cannot determine the intended structure of this "
            "statement. In a permissive runtime, execution could branch "
            "unpredictably, variables may be unbound, and exceptions may "
            "propagate unhandled."
        ),
    },
}

_FALLBACK_PATTERN: Dict[str, str] = {
    'severity_label': 'INFO',
    'title':         'Syntax Error',
    'why_unsafe':    'Could not be mapped to a known unsafe pattern.',
}

# Human-readable fix strings for each fix action token
_FIX_DESCRIPTIONS: Dict[str, str] = {
    'ADD_COLON_BLOCK_HEADER':    "Add ':' at the end of the block header statement.",
    'ADD_COLON_DEF':             "Add ':' after the function definition header: def name():",
    'ADD_COLON_IF':              "Add ':' after the if/elif/else condition: if condition:",
    'ADD_COLON_FOR':             "Add ':' after the for clause: for x in items:",
    'ADD_COLON_WHILE':           "Add ':' after the while condition: while condition:",
    'CLOSE_PAREN':               "Add the missing closing parenthesis ')'. Check every func().",
    'CLOSE_BRACKET':             "Add the missing closing bracket ']'. Check every list[].",
    'CLOSE_BRACE':               "Add the missing closing brace '}'. Check every dict{}.",
    'FIX_INDENTATION_SPACES':    "Re-align to exactly 4 spaces per indentation level (PEP 8).",
    'FIX_MIXED_TABS_SPACES':     "Convert all tabs to spaces. Never mix tabs and spaces.",
    'COMPLETE_ASSIGNMENT_RHS':   "Complete the assignment: x = <value>.",
    'COMPLETE_RETURN_VALUE':     "Provide a return value if one is expected: return <value>.",
    'MOVE_STATEMENT_OUT':        "This statement is in an invalid context — move it out.",
    'FIX_OPERATOR_SYNTAX':       "Remove or correct the invalid operator combination.",
    'FIX_KEYWORD_AS_IDENTIFIER': "Rename the variable — it shadows a Python keyword.",
}


# ── Result types ──────────────────────────────────────────────────────────────

@dataclass
class FixSuggestion:
    rank:        int
    action:      str
    description: str
    confidence:  float

    def to_dict(self) -> Dict[str, Any]:
        return vars(self)


@dataclass
class Diagnostic:
    line:           int
    column:         int
    error_type:     str
    error_message:  str
    unsafe_pattern: str
    pattern_confidence: float
    severity_label: str
    severity_score: float       # 0–10
    title:          str
    why_unsafe:     str
    top_fixes:      List[FixSuggestion] = field(default_factory=list)
    is_anomalous:   bool = False

    def to_dict(self) -> Dict[str, Any]:
        d = vars(self)
        d['top_fixes'] = [f.to_dict() for f in self.top_fixes]
        return d


@dataclass
class DiagnosticReport:
    filepath:     str
    language:     str
    total_errors: int
    diagnostics:  List[Diagnostic] = field(default_factory=list)

    def summary(self) -> str:
        sep = "─" * 68
        lines = [
            sep,
            "  AI Intelligent Diagnostic Report",
            f"  File    : {self.filepath}",
            f"  Language: {self.language}   |   Errors: {self.total_errors}",
            sep,
        ]
        if not self.diagnostics:
            lines.append("  ✓  No syntax errors detected.")
        else:
            for i, d in enumerate(self.diagnostics, 1):
                anom = " [ANOMALY]" if d.is_anomalous else ""
                lines += [
                    f"\n  [{d.severity_label}]{anom}  Error #{i}  "
                    f"Line {d.line}, Col {d.column}",
                    f"  Parser error      : {d.error_type}",
                    f"  Message           : {d.error_message}",
                    f"  Unsafe pattern    : {d.unsafe_pattern}"
                    f"  (confidence {d.pattern_confidence:.0%})",
                    f"  Risk score        : {d.severity_score:.1f} / 10",
                    f"  Title             : {d.title}",
                    f"  Why it is unsafe  : {d.why_unsafe}",
                    f"  Top-3 fixes:",
                ]
                for fix in d.top_fixes:
                    lines.append(
                        f"    #{fix.rank} ({fix.confidence:.0%})  "
                        f"[{fix.action}] {fix.description}"
                    )
        lines.append("\n" + sep)
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'filepath':     self.filepath,
            'language':     self.language,
            'total_errors': self.total_errors,
            'diagnostics':  [d.to_dict() for d in self.diagnostics],
        }


# ── Engine ────────────────────────────────────────────────────────────────────

class IntelligentDiagnosticsEngine:
    """
    Runtime engine: loads all trained models and generates diagnostics.

    Args:
        model_dir: directory containing model_*.pkl files produced by
                   ml/train_classifier.py  (default: "ml")
    """

    def __init__(self, model_dir: str = "ml"):
        self._clf      = self._load(model_dir, 'model_classifier.pkl')
        self._reg      = self._load(model_dir, 'model_severity.pkl')
        self._fix      = self._load(model_dir, 'model_fix_ranker.pkl')
        self._anomaly  = self._load(model_dir, 'model_anomaly.pkl',
                                    required=False)
        self._fix_classes: List[str] = (
            list(self._fix.classes_)
            if hasattr(self._fix, 'classes_') else
            list(self._fix.named_steps['clf'].classes_)
        )

    @staticmethod
    def _load(model_dir: str, fname: str, required: bool = True):
        path = os.path.join(model_dir, fname)
        if not os.path.exists(path):
            if required:
                raise FileNotFoundError(
                    f"Model not found: '{path}'. Run:  python -m ml.train_classifier"
                )
            return None
        import sys
        import ml.train_classifier as _tc
        # Make custom transformers resolvable regardless of how pickle stored them.
        # When train_classifier was run as __main__ it pickled classes under
        # '__main__' module; we alias them here so pickle.load() can find them.
        sys.modules.setdefault('__main__', sys.modules[__name__])
        _fake = sys.modules.get('__main__')
        for _attr in ('_TextExtractor', '_NumericExtractor'):
            if not hasattr(_fake, _attr):
                setattr(_fake, _attr, getattr(_tc, _attr))
        with open(path, 'rb') as f:
            return pickle.load(f)

    # ── Public API ─────────────────────────────────────────────────────────

    def analyse(self, filepath: str, language: str = 'python') -> DiagnosticReport:
        source = open(filepath, encoding='utf-8', errors='ignore').read()
        return self.analyse_source(source, filepath=filepath, language=language)

    def analyse_source(self,
                       source:   str,
                       filepath: str = "<string>",
                       language: str = 'python') -> DiagnosticReport:

        # Step 1 – lex + parse
        tokens           = tokenize_python(source)
        ast_tree, errors = parse_python(tokens)

        report = DiagnosticReport(
            filepath=filepath,
            language=language,
            total_errors=len(errors),
        )

        if not errors:
            return report

        # Step 2 – extract features
        extractor    = ASTFeatureExtractor(tokens, ast_tree)
        feature_list = extractor.extract(errors)

        # Step 3 – pattern classification (calibrated probabilities)
        patterns    = self._clf.predict(feature_list)
        probas      = self._clf.predict_proba(feature_list)   # shape (N, C)
        clf_classes = list(self._clf.classes_)
        confidences = probas.max(axis=1)

        # Step 4 – severity scores
        sev_scores = np.clip(self._reg.predict(feature_list), 0, 10)

        # Step 5 – fix ranking (top-3)
        fix_probas   = self._fix.predict_proba(feature_list)  # shape (N, F)

        # Step 6 – anomaly scores (per-file, applied to all errors in file)
        is_anomalous = False
        if self._anomaly is not None:
            try:
                num_feat = _NumericExtractor().transform(feature_list)
                # Anomaly score: negative = anomalous
                file_score = self._anomaly.decision_function(
                    num_feat.mean(axis=0, keepdims=True)
                )
                is_anomalous = bool(file_score[0] < 0)
            except Exception:
                pass

        # Step 7 – assemble diagnostics
        for err, pattern, confidence, sev, fp in zip(
            errors, patterns, confidences, sev_scores, fix_probas
        ):
            info = _PATTERNS.get(pattern, _FALLBACK_PATTERN)

            # Top-3 fix suggestions
            top3_idx = np.argsort(fp)[::-1][:3]
            top_fixes = []
            for rank, fix_i in enumerate(top3_idx, 1):
                if fix_i < len(self._fix_classes):
                    action = self._fix_classes[fix_i]
                    top_fixes.append(FixSuggestion(
                        rank        = rank,
                        action      = action,
                        description = _FIX_DESCRIPTIONS.get(action, action),
                        confidence  = float(fp[fix_i]),
                    ))

            report.diagnostics.append(Diagnostic(
                line               = err.line,
                column             = err.column,
                error_type         = err.error_type,
                error_message      = err.message,
                unsafe_pattern     = pattern,
                pattern_confidence = float(confidence),
                severity_label     = info['severity_label'],
                severity_score     = float(sev),
                title              = info['title'],
                why_unsafe         = info['why_unsafe'],
                top_fixes          = top_fixes,
                is_anomalous       = is_anomalous,
            ))

        return report
