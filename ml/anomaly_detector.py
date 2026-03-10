"""
Anomaly Detector — Structurally Risky but Syntactically Valid Code
===================================================================
An Isolation Forest trained on valid Python files detects code that:
  • Parses without errors
  • But has unusual structural properties compared to the valid-code training set

This catches patterns like:
  • Extremely high nesting in a function with no return
  • Deeply nested loops with no break/continue
  • Very low keyword density (obfuscated code)
  • Delimiter counts far outside the normal range

Usage:
    detector = AnomalyDetector()

    # Analyse a source string
    result = detector.analyse_source(source_code)
    print(result.summary())

    # Or analyse a file
    result = detector.analyse("my_file.py")
"""

from __future__ import annotations

import os
import pickle
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import numpy as np

from lexers import tokenize_python
from parsers import parse_python
from ml.ast_feature_extractor import ASTFeatureExtractor, ErrorFeatures
from ml.train_classifier import _NumericExtractor


# ── Result type ───────────────────────────────────────────────────────────────

@dataclass
class AnomalyResult:
    filepath:         str
    is_anomalous:     bool
    anomaly_score:    float      # positive = normal, negative = anomalous
    risk_flags:       List[str]  # human-readable reasons
    structural_stats: Dict[str, Any]

    def summary(self) -> str:
        verdict = "ANOMALOUS" if self.is_anomalous else "NORMAL"
        sep = "─" * 60
        lines = [
            sep,
            f"  Anomaly Detection Report — {verdict}",
            f"  File         : {self.filepath}",
            f"  Anomaly score: {self.anomaly_score:+.4f}  "
            f"(negative = anomalous)",
        ]
        if self.risk_flags:
            lines.append("  Risk flags:")
            for flag in self.risk_flags:
                lines.append(f"    • {flag}")
        lines.append("  Structural stats:")
        for k, v in self.structural_stats.items():
            lines.append(f"    {k}: {v}")
        lines.append(sep)
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'filepath':         self.filepath,
            'is_anomalous':     self.is_anomalous,
            'anomaly_score':    self.anomaly_score,
            'risk_flags':       self.risk_flags,
            'structural_stats': self.structural_stats,
        }


# ── Rule-based flags (threshold checks on structural features) ────────────────

_RISK_RULES = [
    # (field_name, operator, threshold, message)
    ('max_nesting_depth',   '>', 6,     "Max nesting depth > 6"),
    ('keyword_density',     '<', 0.02,  "Very low keyword density (< 2% of tokens)"),
    ('delimiter_imbalance', '>', 3,     "Delimiter imbalance > 3 (unbalanced brackets)"),
    ('num_functions',       '>', 20,    "More than 20 function definitions"),
    ('total_statements',    '>', 200,   "More than 200 top-level statements"),
]

_OPS = {
    '>': lambda a, b: a > b,
    '<': lambda a, b: a < b,
    '>=': lambda a, b: a >= b,
    '<=': lambda a, b: a <= b,
}


def _check_risk_flags(feat: ErrorFeatures) -> List[str]:
    flags = []
    for field_name, op, threshold, msg in _RISK_RULES:
        val = getattr(feat, field_name, None)
        if val is not None and _OPS[op](val, threshold):
            flags.append(msg)
    return flags


# ── Detector ──────────────────────────────────────────────────────────────────

class AnomalyDetector:
    """
    Wraps the Isolation Forest model trained on valid code.

    Falls back gracefully if the model file does not exist (reports rule-based
    flags only with a neutral score).

    Args:
        model_dir: directory containing model_anomaly.pkl
    """

    def __init__(self, model_dir: str = "ml"):
        self._iso       = self._load(model_dir)
        self._extractor = _NumericExtractor()

    @staticmethod
    def _load(model_dir: str):
        path = os.path.join(model_dir, 'model_anomaly.pkl')
        if not os.path.exists(path):
            return None
        with open(path, 'rb') as f:
            return pickle.load(f)

    # ── Public API ─────────────────────────────────────────────────────────

    def analyse(self, filepath: str) -> AnomalyResult:
        source = open(filepath, encoding='utf-8', errors='ignore').read()
        return self.analyse_source(source, filepath=filepath)

    def analyse_source(self,
                       source:   str,
                       filepath: str = "<string>") -> AnomalyResult:
        """
        Run Isolation Forest + rule-based flag checks on a source file.
        """
        tokens           = tokenize_python(source)
        ast_tree, errors = parse_python(tokens)

        # Build a single file-level ErrorFeatures (no actual errors needed)
        feat = ErrorFeatures(errors_total=len(errors))
        ext  = ASTFeatureExtractor(tokens, ast_tree)
        ext._fill_struct(feat)
        ext._fill_tok_stats(feat)

        # Rule-based flags
        risk_flags = _check_risk_flags(feat)

        # Isolation Forest score
        anomaly_score = 0.0
        is_anomalous  = False

        if self._iso is not None:
            try:
                X               = self._extractor.transform([feat])
                X               = np.nan_to_num(X, nan=0.0)
                raw_score       = self._iso.decision_function(X)[0]
                anomaly_score   = float(raw_score)
                is_anomalous    = anomaly_score < 0.0
            except Exception:
                pass
        else:
            # No model available — fall back to rule-based only
            is_anomalous = len(risk_flags) >= 2

        structural_stats = {
            'num_functions':      feat.num_functions,
            'num_loops':          feat.num_loops,
            'num_if_stmts':       feat.num_if_stmts,
            'max_nesting_depth':  feat.max_nesting_depth,
            'total_statements':   feat.total_statements,
            'total_tokens':       feat.total_tokens,
            'keyword_density':    round(feat.keyword_density, 4),
            'delimiter_imbalance':feat.delimiter_imbalance,
            'errors_found':       feat.errors_total,
        }

        return AnomalyResult(
            filepath         = filepath,
            is_anomalous     = is_anomalous,
            anomaly_score    = anomaly_score,
            risk_flags       = risk_flags,
            structural_stats = structural_stats,
        )
