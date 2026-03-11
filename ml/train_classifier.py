"""
ML Training Pipeline
====================
Trains the full suite of models from datasets/*/invalid/ and datasets/*/valid/:

  Model 1 â€“ Pattern Classifier
      VotingClassifier(LogisticRegression + RandomForest)
      wrapped in CalibratedClassifierCV for accurate probabilities.
      Features: TF-IDF(text) + StandardScaler(numeric + co-occurrence)

  Model 2 â€“ Severity Regressor
      Ridge regression predicts a 0-10 risk score per error.

  Model 3 â€“ Fix Ranker
      Multi-label LogisticRegression that ranks the top-3 specific fix actions.

  Model 4 â€“ Isolation Forest (anomaly detector for valid-looking code)
      Saved separately; used by AnomalyDetector at runtime.

Run directly:
    python -m ml.train_classifier
"""

from __future__ import annotations

import os
import re
import pickle
from typing import Any, Dict, List, Tuple

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import RandomForestClassifier, VotingClassifier, IsolationForest
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, Ridge, SGDClassifier
from sklearn.metrics import classification_report, mean_absolute_error
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import StandardScaler

from lexers import tokenize_python
from parsers import parse_python
from ml.ast_feature_extractor import (
    ASTFeatureExtractor, ErrorFeatures,
    LABEL_MAP, ALL_LABELS, ALL_ERROR_TYPES, SEVERITY_BASE,
)

# â”€â”€ Fix action vocabulary â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

# Each "fix action" is a short unique token that the fix-ranker learns to predict.
# Diagnostic engine maps these back to human-readable strings.
FIX_ACTIONS: List[str] = [
    'ADD_COLON_BLOCK_HEADER',       # add : after if/for/while/def/class
    'ADD_COLON_DEF',                # specifically after def
    'ADD_COLON_IF',                 # specifically after if / elif / else
    'ADD_COLON_FOR',                # specifically after for
    'ADD_COLON_WHILE',              # specifically after while
    'CLOSE_PAREN',                  # add missing )
    'CLOSE_BRACKET',                # add missing ]
    'CLOSE_BRACE',                  # add missing }
    'FIX_INDENTATION_SPACES',       # re-align to 4-space indent
    'FIX_MIXED_TABS_SPACES',        # convert tabs to spaces
    'COMPLETE_ASSIGNMENT_RHS',      # add right-hand side to assignment
    'COMPLETE_RETURN_VALUE',        # add value after return
    'MOVE_STATEMENT_OUT',           # statement used in wrong scope
    'FIX_OPERATOR_SYNTAX',          # invalid operator combination
    'FIX_KEYWORD_AS_IDENTIFIER',    # rename variable that shadows keyword
]

_FIX_FOR_PATTERN: Dict[str, List[str]] = {
    'UNSAFE_BLOCK_SCOPE':          ['ADD_COLON_BLOCK_HEADER', 'ADD_COLON_DEF',
                                    'ADD_COLON_IF', 'ADD_COLON_FOR', 'ADD_COLON_WHILE'],
    'UNSAFE_EXPRESSION_BOUNDARY':  ['CLOSE_PAREN', 'CLOSE_BRACKET', 'CLOSE_BRACE'],
    'UNSAFE_SCOPE_LEAK':           ['FIX_INDENTATION_SPACES', 'FIX_MIXED_TABS_SPACES'],
    'UNSAFE_INCOMPLETE_OPERATION': ['COMPLETE_ASSIGNMENT_RHS', 'COMPLETE_RETURN_VALUE',
                                    'MOVE_STATEMENT_OUT'],
    'UNSAFE_UNDEFINED_BEHAVIOR':   ['FIX_OPERATOR_SYNTAX', 'FIX_KEYWORD_AS_IDENTIFIER',
                                    'MOVE_STATEMENT_OUT'],
}

# â”€â”€ Dataset construction â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

_FNAME_RE = re.compile(r"invalid_([a-z_]+)_\d+\.\w+$")


def _label_from_filename(fname: str):
    m = _FNAME_RE.search(fname)
    return m.group(1) if m else None


def _parse_file(fpath: str):
    """Tokenize + parse one file; return (tokens, ast_tree, errors)."""
    source = open(fpath, encoding='utf-8', errors='ignore').read()
    tokens = tokenize_python(source)
    ast_tree, errors = parse_python(tokens)
    return tokens, ast_tree, errors


def build_invalid_dataset(dataset_dir: str = "datasets") -> List[ErrorFeatures]:
    """
    Parse all invalid Python files, extract features, return labeled samples.
    """
    all_features: List[ErrorFeatures] = []
    invalid_dir = os.path.join(dataset_dir, 'python', 'invalid')

    files = sorted(os.listdir(invalid_dir))
    print(f"  Parsing {len(files)} invalid files â€¦")

    for fname in files:
        raw_label = _label_from_filename(fname)
        if raw_label is None or raw_label not in LABEL_MAP:
            continue

        fpath = os.path.join(invalid_dir, fname)
        try:
            tokens, ast_tree, errors = _parse_file(fpath)
        except Exception:
            continue

        if not errors:
            continue

        extractor = ASTFeatureExtractor(tokens, ast_tree)
        feats     = extractor.extract(errors, label=raw_label)
        all_features.extend(feats)

    return all_features


def build_valid_numeric_features(dataset_dir: str = "datasets") -> np.ndarray:
    """
    Parse valid Python files and return numeric feature matrix for anomaly
    detection (Isolation Forest training).
    """
    rows: List[List[float]] = []
    valid_dir = os.path.join(dataset_dir, 'python', 'valid')
    files     = sorted(os.listdir(valid_dir))
    print(f"  Parsing {len(files)} valid files for anomaly model â€¦")

    extractor_cls = _NumericExtractor()

    for fname in files:
        fpath = os.path.join(valid_dir, fname)
        try:
            tokens, ast_tree, _ = _parse_file(fpath)
        except Exception:
            continue

        # Dummy ErrorFeatures representing the file-level structure
        dummy = ErrorFeatures()
        ext   = ASTFeatureExtractor(tokens, ast_tree)
        ext._fill_struct(dummy)
        ext._fill_tok_stats(dummy)
        rows.append([getattr(dummy, f, 0) for f in _NumericExtractor._FIELDS])

    return np.array(rows, dtype=float) if rows else np.zeros((1, len(_NumericExtractor._FIELDS)))


# â”€â”€ Custom sklearn transformers â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class _TextExtractor(BaseEstimator, TransformerMixin):
    """Concatenates all text fields of ErrorFeatures for TF-IDF ingestion."""

    def fit(self, X, y=None):
        return self

    def transform(self, X: List[ErrorFeatures]):
        return [
            " ".join([
                f.error_type,
                f.error_message,
                f.error_token,
                f.token_window,
                f.nearby_keywords,
                f.ast_path,
            ])
            for f in X
        ]


class _NumericExtractor(BaseEstimator, TransformerMixin):
    """Extracts numeric structural fields + co-occurrence vector."""

    _FIELDS = [
        'num_functions', 'num_if_stmts', 'num_loops',
        'max_nesting_depth', 'total_statements', 'errors_total',
        'total_tokens', 'keyword_density', 'delimiter_imbalance',
        'error_nesting_depth', 'error_inside_function',
        'error_inside_loop', 'has_try_keyword_nearby',
    ]

    def fit(self, X, y=None):
        return self

    def transform(self, X: List[ErrorFeatures]):
        numeric = np.array(
            [[getattr(f, field, 0) for field in self._FIELDS] for f in X],
            dtype=float,
        )
        co_occ = np.array([f.co_occurrence for f in X], dtype=float)
        return np.hstack([numeric, co_occ])


# â”€â”€ Pipeline builders â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def _build_feature_union() -> FeatureUnion:
    return FeatureUnion([
        ('text', Pipeline([
            ('extract', _TextExtractor()),
            ('tfidf',   TfidfVectorizer(
                ngram_range=(1, 2),
                max_features=5_000,
                sublinear_tf=True,
                min_df=2,
            )),
        ])),
        ('numeric', Pipeline([
            ('extract', _NumericExtractor()),
            ('scale',   StandardScaler()),
        ])),
    ])


def build_pattern_classifier() -> Pipeline:
    """
    VotingClassifier (LR + RF) wrapped in Platt-scaling calibration.
    """
    lr = LogisticRegression(max_iter=1000, C=1.0, class_weight='balanced',
                            solver='lbfgs', n_jobs=-1)
    rf = RandomForestClassifier(n_estimators=100, max_depth=12,
                                class_weight='balanced', random_state=42,
                                n_jobs=-1)
    voting = VotingClassifier(
        estimators=[('lr', lr), ('rf', rf)],
        voting='soft', n_jobs=-1,
    )
    calibrated = CalibratedClassifierCV(voting, cv=2, method='sigmoid')

    return Pipeline([
        ('features', _build_feature_union()),
        ('clf',      calibrated),
    ])


def build_severity_regressor() -> Pipeline:
    """Ridge regressor predicting a 0-10 risk score."""
    return Pipeline([
        ('features', _build_feature_union()),
        ('reg',      Ridge(alpha=1.0)),
    ])


def build_fix_ranker() -> Pipeline:
    """
    Multi-class classifier that predicts the single most likely fix action.
    (Top-3 are retrieved from predict_proba at inference time.)
    """
    return Pipeline([
        ('features', _build_feature_union()),
        ('clf',      LogisticRegression(
            max_iter=1000, C=0.5,
            class_weight='balanced',
            solver='lbfgs',
        )),
    ])


# â”€â”€ Training orchestration â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def _derive_fix_label(feat: ErrorFeatures) -> str:
    """Return the primary fix action for a given labeled ErrorFeature."""
    fixes = _FIX_FOR_PATTERN.get(feat.label, [])
    if not fixes:
        return 'FIX_OPERATOR_SYNTAX'

    # Heuristic: pick more specific fix based on nearby_keywords
    kw = feat.nearby_keywords
    if feat.label == 'UNSAFE_BLOCK_SCOPE':
        if 'def'   in kw: return 'ADD_COLON_DEF'
        if 'if'    in kw or 'elif' in kw or 'else' in kw: return 'ADD_COLON_IF'
        if 'for'   in kw: return 'ADD_COLON_FOR'
        if 'while' in kw: return 'ADD_COLON_WHILE'
        return 'ADD_COLON_BLOCK_HEADER'

    return fixes[0]


def train(dataset_dir: str = "datasets",
          output_dir:  str = "ml") -> None:

    os.makedirs(output_dir, exist_ok=True)

    # â”€â”€ Step 1: Build dataset â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    print("\n[1/5] Building invalid-code dataset â€¦")
    features = build_invalid_dataset(dataset_dir)
    if not features:
        print("ERROR: No training samples found. Check datasets/python/invalid/")
        return

    labels   = [f.label for f in features]
    severity = [f.severity_score for f in features]
    fix_lbls = [_derive_fix_label(f) for f in features]

    unique_labels = sorted(set(labels))
    print(f"  {len(features)} samples | {len(unique_labels)} pattern classes")
    for lbl in unique_labels:
        print(f"    {lbl}: {labels.count(lbl)} samples")

    # Stratification guard
    counts   = {l: labels.count(l) for l in unique_labels}
    stratify = labels if all(c >= 3 for c in counts.values()) else None

    X_tr, X_te, y_tr, y_te, sev_tr, sev_te, fix_tr, fix_te = train_test_split(
        features, labels, severity, fix_lbls,
        test_size=0.2, random_state=42, stratify=stratify,
    )

    # â”€â”€ Step 2: Pattern classifier â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    print("\n[2/5] Training pattern classifier (LR+RF ensemble + calibration) â€¦")
    clf_pipeline = build_pattern_classifier()
    clf_pipeline.fit(X_tr, y_tr)

    y_pred = clf_pipeline.predict(X_te)
    print("\n  Held-out Classification Report:")
    print(classification_report(y_te, y_pred, zero_division=0))

    cv_scores = cross_val_score(clf_pipeline, features, labels,
                                cv=3, scoring='f1_macro', n_jobs=-1)
    print(f"  3-fold macro-F1: {cv_scores.mean():.3f} +/- {cv_scores.std():.3f}")

    clf_path = os.path.join(output_dir, 'model_classifier.pkl')
    with open(clf_path, 'wb') as f:
        pickle.dump(clf_pipeline, f)
    print(f"  Saved â†’ {clf_path}")

    # â”€â”€ Step 3: Severity regressor â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    print("\n[3/5] Training severity regressor â€¦")
    reg_pipeline = build_severity_regressor()
    reg_pipeline.fit(X_tr, sev_tr)

    sev_pred = reg_pipeline.predict(X_te)
    sev_pred = np.clip(sev_pred, 0, 10)
    mae = mean_absolute_error(sev_te, sev_pred)
    print(f"  Held-out MAE: {mae:.3f} (scale 0-10)")

    reg_path = os.path.join(output_dir, 'model_severity.pkl')
    with open(reg_path, 'wb') as f:
        pickle.dump(reg_pipeline, f)
    print(f"  Saved â†’ {reg_path}")

    # â”€â”€ Step 4: Fix ranker â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    print("\n[4/5] Training fix ranker â€¦")
    fix_pipeline = build_fix_ranker()
    fix_pipeline.fit(X_tr, fix_tr)

    fix_pred = fix_pipeline.predict(X_te)
    print(classification_report(fix_te, fix_pred, zero_division=0))

    fix_path = os.path.join(output_dir, 'model_fix_ranker.pkl')
    with open(fix_path, 'wb') as f:
        pickle.dump(fix_pipeline, f)
    print(f"  Saved â†’ {fix_path}")

    # â”€â”€ Step 5: Isolation Forest (anomaly detection on valid code) â”€â”€â”€â”€â”€â”€â”€â”€â”€
    print("\n[5/5] Training Isolation Forest on valid code â€¦")
    valid_X = build_valid_numeric_features(dataset_dir)
    if valid_X.shape[0] > 1:
        iso = IsolationForest(
            n_estimators=100,
            contamination=0.05,
            random_state=42,
            n_jobs=-1,
        )
        iso.fit(valid_X)
        iso_path = os.path.join(output_dir, 'model_anomaly.pkl')
        with open(iso_path, 'wb') as f:
            pickle.dump(iso, f)
        print(f"  Trained on {valid_X.shape[0]} valid files. Saved â†’ {iso_path}")
    else:
        print("  Skipped: not enough valid files.")

    # â”€â”€ Save SGDClassifier skeleton for online learning â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    from sklearn.utils.class_weight import compute_class_weight
    import numpy as _np2
    classes_arr = _np2.array(ALL_LABELS)
    cw_vals = compute_class_weight('balanced', classes=classes_arr, y=y_tr)
    cw_dict = dict(zip(ALL_LABELS, cw_vals))
    sgd = SGDClassifier(loss='log_loss', max_iter=1000, class_weight=cw_dict,
                        random_state=42)
    sgd.partial_fit(
        _NumericExtractor().transform(X_tr),
        y_tr,
        classes=ALL_LABELS,
    )
    sgd_path = os.path.join(output_dir, 'model_online.pkl')
    with open(sgd_path, 'wb') as f:
        pickle.dump(sgd, f)
    print(f"\n  Online SGD model saved â†’ {sgd_path}")

    print("\nâœ“ All models trained successfully.")


if __name__ == "__main__":
    train()

