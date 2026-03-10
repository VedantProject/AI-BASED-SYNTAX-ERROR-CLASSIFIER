"""
Batch Analyzer — Cross-File Root-Cause Clustering
===================================================
Parses a directory of source files, runs the full ML pipeline on every file,
then uses K-Means to cluster errors by their root cause.

Errors that cluster together across different files share structural patterns
(same nesting depth, same AST path, same error co-occurrence profile) — this
suggests a systemic coding issue rather than one-off mistakes.

Output:
  BatchAnalysisReport — contains per-file diagnostics + cluster assignments
  A summary table mapping cluster_id → dominant pattern + typical fix

Usage:
    analyzer = BatchAnalyzer()
    report   = analyzer.analyse_directory("datasets/python/invalid")
    print(report.summary())
    report.save_json("results/batch_ml/report.json")
"""

from __future__ import annotations

import json
import os
from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from lexers import tokenize_python
from parsers import parse_python
from ml.ast_feature_extractor import ASTFeatureExtractor, ErrorFeatures
from ml.intelligent_diagnostics import IntelligentDiagnosticsEngine, DiagnosticReport
from ml.train_classifier import _NumericExtractor


# ── Data types ────────────────────────────────────────────────────────────────

@dataclass
class ClusterSummary:
    cluster_id:       int
    size:             int
    dominant_pattern: str
    dominant_fix:     str
    file_count:       int
    avg_severity:     float
    representative_errors: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = vars(self)
        return d


@dataclass
class BatchAnalysisReport:
    directory:      str
    total_files:    int
    total_errors:   int
    num_clusters:   int
    file_reports:   List[DiagnosticReport] = field(default_factory=list)
    cluster_map:    Dict[str, int]         = field(default_factory=dict)   # filepath → cluster_id
    cluster_summaries: List[ClusterSummary]= field(default_factory=list)

    def summary(self) -> str:
        sep = "═" * 68
        lines = [
            sep,
            "  AI Batch Analysis Report — Root-Cause Clustering",
            f"  Directory : {self.directory}",
            f"  Files     : {self.total_files}   |   Errors: {self.total_errors}"
            f"   |   Clusters: {self.num_clusters}",
            sep,
        ]
        for cs in self.cluster_summaries:
            lines += [
                f"\n  Cluster #{cs.cluster_id}  ({cs.size} errors across {cs.file_count} files)",
                f"    Dominant pattern : {cs.dominant_pattern}",
                f"    Primary fix      : {cs.dominant_fix}",
                f"    Avg risk score   : {cs.avg_severity:.1f} / 10",
                f"    Sample errors:",
            ]
            for err in cs.representative_errors[:3]:
                lines.append(
                    f"      • {err.get('filepath','?')} line {err.get('line','?')}"
                    f" — {err.get('error_type','?')}"
                )
        lines.append("\n" + sep)
        return "\n".join(lines)

    def save_json(self, path: str) -> None:
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        data = {
            'directory':    self.directory,
            'total_files':  self.total_files,
            'total_errors': self.total_errors,
            'num_clusters': self.num_clusters,
            'cluster_map':  self.cluster_map,
            'cluster_summaries': [c.to_dict() for c in self.cluster_summaries],
            'file_reports': [r.to_dict() for r in self.file_reports],
        }
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Saved batch report → {path}")


# ── Analyzer ──────────────────────────────────────────────────────────────────

class BatchAnalyzer:
    """
    Runs IntelligentDiagnosticsEngine on every file in a directory, then
    clusters errors with K-Means to identify systemic root causes.

    Args:
        model_dir:   path to the ml/ directory with trained model pkls
        n_clusters:  K for K-Means (auto if None)
    """

    def __init__(self,
                 model_dir:  str = "ml",
                 n_clusters: Optional[int] = None):
        self._engine     = IntelligentDiagnosticsEngine(model_dir=model_dir)
        self._n_clusters = n_clusters
        self._extractor  = _NumericExtractor()

    # ── Public API ─────────────────────────────────────────────────────────

    def analyse_directory(self,
                           directory:  str,
                           extensions: Tuple[str, ...] = ('.py',)) -> BatchAnalysisReport:
        """
        Parse all source files in directory, run ML diagnostics, cluster errors.
        """
        files = [
            os.path.join(directory, f)
            for f in sorted(os.listdir(directory))
            if any(f.endswith(ext) for ext in extensions)
        ]

        print(f"  Analysing {len(files)} files in {directory} …")

        all_reports:   List[DiagnosticReport] = []
        all_features:  List[ErrorFeatures]    = []
        all_meta:      List[Dict[str, Any]]   = []   # aligned with all_features

        for fpath in files:
            try:
                source   = open(fpath, encoding='utf-8', errors='ignore').read()
                tokens   = tokenize_python(source)
                ast_tree, errors = parse_python(tokens)

                report = self._engine.analyse_source(
                    source, filepath=fpath, language='python'
                )
                all_reports.append(report)

                if errors:
                    extractor = ASTFeatureExtractor(tokens, ast_tree)
                    feats     = extractor.extract(errors)
                    for feat, diag in zip(feats, report.diagnostics):
                        all_features.append(feat)
                        all_meta.append({
                            'filepath':   fpath,
                            'line':       diag.line,
                            'error_type': diag.error_type,
                            'pattern':    diag.unsafe_pattern,
                            'fix':        diag.top_fixes[0].action if diag.top_fixes else '',
                            'severity':   diag.severity_score,
                        })

            except Exception as exc:
                print(f"    [skip] {fpath}: {exc}")

        total_errors = len(all_features)
        report_obj   = BatchAnalysisReport(
            directory=directory,
            total_files=len(all_reports),
            total_errors=total_errors,
            num_clusters=0,
            file_reports=all_reports,
        )

        if total_errors < 2:
            print("  Not enough errors to cluster.")
            return report_obj

        # ── K-Means clustering ─────────────────────────────────────────────
        X = self._extractor.transform(all_features).astype(float)

        # Replace any NaN/Inf that slipped through
        X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)

        scaler = StandardScaler()
        X_sc   = scaler.fit_transform(X)

        k = self._n_clusters or self._auto_k(total_errors)
        k = min(k, total_errors)

        km = KMeans(n_clusters=k, random_state=42, n_init='auto')
        labels = km.fit_predict(X_sc)

        print(f"  K-Means: k={k}, inertia={km.inertia_:.1f}")

        # ── Build cluster summaries ────────────────────────────────────────
        cluster_map: Dict[str, int] = {}
        clusters:    Dict[int, List[Dict]] = {i: [] for i in range(k)}

        for meta, cluster_id in zip(all_meta, labels):
            clusters[int(cluster_id)].append(meta)
            fp = meta['filepath']
            # A file is associated with the cluster of its first error
            if fp not in cluster_map:
                cluster_map[fp] = int(cluster_id)

        summaries: List[ClusterSummary] = []
        for cid in sorted(clusters.keys()):
            members = clusters[cid]
            if not members:
                continue

            patterns  = [m['pattern']  for m in members]
            fixes     = [m['fix']      for m in members]
            severities= [m['severity'] for m in members]
            filepaths = list({m['filepath'] for m in members})

            dom_pattern = Counter(patterns).most_common(1)[0][0]
            dom_fix     = Counter(f for f in fixes if f).most_common(1)
            dom_fix_str = dom_fix[0][0] if dom_fix else '—'

            summaries.append(ClusterSummary(
                cluster_id       = cid,
                size             = len(members),
                dominant_pattern = dom_pattern,
                dominant_fix     = dom_fix_str,
                file_count       = len(filepaths),
                avg_severity     = float(np.mean(severities)),
                representative_errors = members[:5],
            ))

        summaries.sort(key=lambda c: c.size, reverse=True)

        report_obj.num_clusters      = k
        report_obj.cluster_map       = cluster_map
        report_obj.cluster_summaries = summaries

        return report_obj

    # ── Helpers ────────────────────────────────────────────────────────────

    @staticmethod
    def _auto_k(n_errors: int) -> int:
        """Heuristic: ~1 cluster per 30 errors, bounded [2, 10]."""
        return max(2, min(10, n_errors // 30))
