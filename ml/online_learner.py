"""
Online Learner — Incremental Model Improvement
===============================================
Uses SGDClassifier.partial_fit() to update the model from user corrections
without retraining from scratch.

When users confirm or correct a pattern classification, that feedback is:
  1. Appended to ml/feedback_log.jsonl
  2. Used to immediately update model_online.pkl via partial_fit()

The online model runs alongside the main classifier.
When they disagree, the online model's vote is a tie-breaker weighted by
how many feedback samples it has learned from.

Usage:
    learner = OnlineLearner()

    # Record user correction (label is the correct pattern name)
    learner.record_feedback(features, correct_label="UNSAFE_SCOPE_LEAK")

    # Predict using the online model
    prediction = learner.predict([features])

    # Save updated model back to disk
    learner.save()
"""

from __future__ import annotations

import json
import os
import pickle
from datetime import datetime
from typing import Dict, List, Optional

import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler

from ml.ast_feature_extractor import ErrorFeatures, ALL_LABELS
from ml.train_classifier import _NumericExtractor


class OnlineLearner:
    """
    Incremental SGD-based classifier that updates from user feedback.

    Args:
        model_dir:    directory containing model_online.pkl
        feedback_log: path to JSONL file where feedback events are stored
    """

    def __init__(self,
                 model_dir:    str = "ml",
                 feedback_log: str = "ml/feedback_log.jsonl"):
        self._model_dir    = model_dir
        self._feedback_log = feedback_log
        self._extractor    = _NumericExtractor()
        self._model        = self._load_or_init()
        self._feedback_count = self._count_existing_feedback()

    # ── Public API ─────────────────────────────────────────────────────────

    def record_feedback(self,
                        feature: ErrorFeatures,
                        correct_label: str) -> None:
        """
        Record a user correction and immediately update the online model.

        Args:
            feature:       ErrorFeatures object for the misclassified error
            correct_label: the correct unsafe pattern name (e.g. UNSAFE_SCOPE_LEAK)
        """
        if correct_label not in ALL_LABELS:
            raise ValueError(
                f"Unknown label '{correct_label}'. "
                f"Valid: {ALL_LABELS}"
            )

        # Update model
        X = self._extractor.transform([feature])
        self._model.partial_fit(X, [correct_label], classes=ALL_LABELS)
        self._feedback_count += 1

        # Persist feedback event
        self._append_feedback(feature, correct_label)
        self.save()

    def predict(self, features: List[ErrorFeatures]) -> List[str]:
        """Predict pattern classes using the online model."""
        X = self._extractor.transform(features)
        return list(self._model.predict(X))

    def predict_proba(self, features: List[ErrorFeatures]) -> np.ndarray:
        """Return class probabilities from the online model."""
        X = self._extractor.transform(features)
        return self._model.predict_proba(X)

    @property
    def feedback_count(self) -> int:
        """Number of feedback samples the online model has learned from."""
        return self._feedback_count

    @property
    def classes(self) -> List[str]:
        return list(self._model.classes_) if hasattr(self._model, 'classes_') else []

    def save(self) -> None:
        """Save current online model to disk."""
        path = os.path.join(self._model_dir, 'model_online.pkl')
        with open(path, 'wb') as f:
            pickle.dump(self._model, f)

    # ── Internal helpers ───────────────────────────────────────────────────

    def _load_or_init(self) -> SGDClassifier:
        path = os.path.join(self._model_dir, 'model_online.pkl')
        if os.path.exists(path):
            with open(path, 'rb') as f:
                return pickle.load(f)

        # Bootstrap with an untrained SGDClassifier that knows the class labels
        sgd = SGDClassifier(
            loss='log_loss',
            max_iter=1000,
            class_weight='balanced',
            random_state=42,
        )
        # Dummy fit so it has classes_ before first partial_fit call
        dummy_X = np.zeros((len(ALL_LABELS), _NumericExtractor._FIELDS.__len__()
                            if hasattr(_NumericExtractor._FIELDS, '__len__')
                            else len(_NumericExtractor._FIELDS)
                            + 19))   # 19 = len(ALL_ERROR_TYPES)
        # Fallback: just use enough columns
        n_cols = len(_NumericExtractor._FIELDS) + 19
        dummy_X = np.zeros((len(ALL_LABELS), n_cols))
        sgd.partial_fit(dummy_X, ALL_LABELS, classes=ALL_LABELS)
        return sgd

    def _count_existing_feedback(self) -> int:
        if not os.path.exists(self._feedback_log):
            return 0
        try:
            with open(self._feedback_log, 'r') as f:
                return sum(1 for line in f if line.strip())
        except Exception:
            return 0

    def _append_feedback(self,
                          feature: ErrorFeatures,
                          correct_label: str) -> None:
        """Append a feedback record to the JSONL log (for audit trail)."""
        os.makedirs(os.path.dirname(self._feedback_log), exist_ok=True)
        record = {
            'timestamp':      datetime.utcnow().isoformat(),
            'correct_label':  correct_label,
            'error_type':     feature.error_type,
            'error_message':  feature.error_message,
            'ast_path':       feature.ast_path,
            'nesting_depth':  feature.error_nesting_depth,
            'inside_function':feature.error_inside_function,
            'inside_loop':    feature.error_inside_loop,
        }
        with open(self._feedback_log, 'a') as f:
            f.write(json.dumps(record) + '\n')

    # ── Feedback statistics ────────────────────────────────────────────────

    def feedback_summary(self) -> Dict[str, int]:
        """Return count of feedback samples per label from the log."""
        counts: Dict[str, int] = {}
        if not os.path.exists(self._feedback_log):
            return counts
        try:
            with open(self._feedback_log) as f:
                for line in f:
                    if not line.strip():
                        continue
                    rec = json.loads(line)
                    lbl = rec.get('correct_label', 'unknown')
                    counts[lbl] = counts.get(lbl, 0) + 1
        except Exception:
            pass
        return counts
