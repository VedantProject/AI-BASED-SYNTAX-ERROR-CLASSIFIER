"""
ML Pipeline Entry Point
========================
Single command-line interface for all ML features.

Commands:
    python -m ml.run_ml check
        Paste your Python code → get errors annotated inline in the source

    python -m ml.run_ml train
        Train all models from datasets/

    python -m ml.run_ml diagnose <file.py>
        Run intelligent diagnostics on a single file

    python -m ml.run_ml batch <directory>
        Batch-analyse a directory + cluster root causes

    python -m ml.run_ml anomaly <file.py>
        Check a valid-looking file for structural anomalies

    python -m ml.run_ml feedback <file.py> <correct_label>
        Record a user correction to improve the online model

    python -m ml.run_ml demo
        Full demo on test_samples/ using all features
"""

from __future__ import annotations

import json
import os
import sys


def _require_args(args: list, n: int, usage: str) -> None:
    if len(args) < n:
        print(f"Usage: {usage}")
        sys.exit(1)


def cmd_check(args: list) -> None:
    """
    Interactive source-code checker.
    Paste Python code, press Enter then Ctrl+Z (Windows) or Ctrl+D (Linux/Mac)
    to finish.  Errors are shown inline within the source, with full AI
    explanations and fix suggestions.
    """
    BORDER = "═" * 68
    THIN   = "─" * 68

    print(BORDER)
    print("  Code Check — AI Syntax Analysis")
    print(BORDER)
    print()
    print("  Paste your Python code below.")
    print("  When done, press  Enter  then  Ctrl+Z  (Windows)")
    print("                         or  Ctrl+D  (Linux / Mac)")
    print()

    try:
        source = sys.stdin.read()
    except (KeyboardInterrupt, EOFError):
        source = ""

    if not source.strip():
        print("  No code provided. Exiting.")
        return

    from ml.intelligent_diagnostics import IntelligentDiagnosticsEngine
    engine = IntelligentDiagnosticsEngine()
    report = engine.analyse_source(source, filepath="<input>", language="python")

    src_lines = source.splitlines()

    print()
    print(BORDER)
    print(f"  Results — {report.total_errors} error(s) found")
    print(BORDER)

    if not report.diagnostics:
        print()
        print("  ✓  No syntax errors detected. Code looks clean!")
        print()
        return

    # Group diagnostics by line number for inline display
    from collections import defaultdict
    by_line: dict = defaultdict(list)
    for d in report.diagnostics:
        by_line[d.line].append(d)

    # ── Annotated source view ─────────────────────────────────────────────
    print()
    print("  ┌─ Annotated Source ")
    print("  │")
    line_w = len(str(len(src_lines)))  # width for line numbers
    for i, code_line in enumerate(src_lines, start=1):
        prefix = f"  │  {str(i).rjust(line_w)} │ "
        print(f"{prefix}{code_line}")
        if i in by_line:
            for d in by_line[i]:
                col  = max(d.column - 1, 0)
                pad  = len(prefix) + col
                arrow_line = " " * pad + "^"
                print(arrow_line)
                indent = " " * (len(prefix) + 1)
                print(f"{indent}└── [{d.severity_label}] {d.error_message}")
    print("  │")
    print("  └" + "─" * 50)

    # ── Per-error detailed explanations ──────────────────────────────────
    print()
    print("  Detailed Explanations")
    print(THIN)
    for idx, d in enumerate(report.diagnostics, 1):
        # Excerpt: the problematic line
        line_text = src_lines[d.line - 1] if 0 < d.line <= len(src_lines) else ""
        col       = max(d.column - 1, 0)
        pointer   = " " * col + "^"

        print()
        print(f"  Error #{idx}  ──  Line {d.line}, Col {d.column}")
        print(f"  {THIN[:50]}")
        print(f"  Source  :  {line_text}")
        print(f"             {pointer}")
        print(f"  Problem :  {d.error_message}")
        print()
        print(f"  Pattern :  {d.unsafe_pattern}  "
              f"(AI confidence: {d.pattern_confidence:.0%})")
        print(f"  Risk    :  {d.severity_score:.1f} / 10  — {d.title}")
        print()
        # Wrap why_unsafe to 65 chars
        why = d.why_unsafe
        words, cur_line, wrapped = why.split(), "", []
        for w in words:
            if len(cur_line) + len(w) + 1 > 65:
                wrapped.append(cur_line.rstrip())
                cur_line = w + " "
            else:
                cur_line += w + " "
        if cur_line.strip():
            wrapped.append(cur_line.rstrip())
        print("  Why it's unsafe:")
        for wl in wrapped:
            print(f"    {wl}")
        print()
        print("  Suggested fixes:")
        for fix in d.top_fixes:
            bar = "█" * int(fix.confidence * 10) + "░" * (10 - int(fix.confidence * 10))
            print(f"    #{fix.rank}  [{bar}] {fix.confidence:.0%}  {fix.description}")
        if idx < len(report.diagnostics):
            print()
            print(f"  {THIN}")
    print()
    print(BORDER)
    print()


def cmd_train(args: list) -> None:
    from ml.train_classifier import train
    dataset_dir = args[0] if args else "datasets"
    output_dir  = args[1] if len(args) > 1 else "ml"
    train(dataset_dir=dataset_dir, output_dir=output_dir)


def cmd_diagnose(args: list) -> None:
    _require_args(args, 1, "python -m ml.run_ml diagnose <file.py>")
    from ml.intelligent_diagnostics import IntelligentDiagnosticsEngine
    engine = IntelligentDiagnosticsEngine()
    report = engine.analyse(args[0])
    print(report.summary())

    out_dir  = "results/ml_diagnostics"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, os.path.basename(args[0]) + "_report.json")
    with open(out_path, 'w') as f:
        json.dump(report.to_dict(), f, indent=2)
    print(f"\nJSON report saved → {out_path}")


def cmd_batch(args: list) -> None:
    _require_args(args, 1, "python -m ml.run_ml batch <directory>")
    from ml.batch_analyzer import BatchAnalyzer
    analyzer = BatchAnalyzer()
    report   = analyzer.analyse_directory(args[0])
    print(report.summary())

    out_dir = "results/ml_batch"
    os.makedirs(out_dir, exist_ok=True)
    report.save_json(os.path.join(out_dir, "batch_report.json"))


def cmd_anomaly(args: list) -> None:
    _require_args(args, 1, "python -m ml.run_ml anomaly <file.py>")
    from ml.anomaly_detector import AnomalyDetector
    detector = AnomalyDetector()
    result   = detector.analyse(args[0])
    print(result.summary())

    out_dir  = "results/ml_anomaly"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, os.path.basename(args[0]) + "_anomaly.json")
    with open(out_path, 'w') as f:
        json.dump(result.to_dict(), f, indent=2)
    print(f"\nJSON report saved → {out_path}")


def cmd_feedback(args: list) -> None:
    _require_args(args, 2,
                  "python -m ml.run_ml feedback <file.py> <correct_label>")
    filepath, correct_label = args[0], args[1]

    from lexers import tokenize_python
    from parsers import parse_python
    from ml.ast_feature_extractor import ASTFeatureExtractor
    from ml.online_learner import OnlineLearner

    source           = open(filepath, encoding='utf-8', errors='ignore').read()
    tokens           = tokenize_python(source)
    ast_tree, errors = parse_python(tokens)

    if not errors:
        print("No parse errors found in file — nothing to correct.")
        return

    extractor    = ASTFeatureExtractor(tokens, ast_tree)
    feature_list = extractor.extract(errors)

    learner = OnlineLearner()
    for feat in feature_list:
        learner.record_feedback(feat, correct_label)

    print(f"Feedback recorded: {len(feature_list)} error(s) labelled as "
          f"'{correct_label}'.")
    print(f"Online model now has {learner.feedback_count} feedback samples.")
    print(f"Feedback log: ml/feedback_log.jsonl")


def cmd_demo(args: list) -> None:
    """Run all features on the test_samples/ directory."""
    print("=" * 68)
    print("  ML Pipeline Demo — All Features")
    print("=" * 68)

    # ── 1. Train if models don't exist ────────────────────────────────────
    if not os.path.exists("ml/model_classifier.pkl"):
        print("\n[Step 1] Training models …")
        from ml.train_classifier import train
        train()
    else:
        print("\n[Step 1] Models already trained. Skipping.")

    # ── 2. Intelligent diagnostics on invalid test ─────────────────────────
    print("\n[Step 2] Intelligent Diagnostics on invalid_test.py …")
    invalid_path = "test_samples/invalid_test.py"
    if os.path.exists(invalid_path):
        from ml.intelligent_diagnostics import IntelligentDiagnosticsEngine
        engine = IntelligentDiagnosticsEngine()
        report = engine.analyse(invalid_path)
        print(report.summary())
    else:
        print(f"  File not found: {invalid_path}")

    # ── 3. Anomaly detection on valid test ─────────────────────────────────
    print("\n[Step 3] Anomaly Detection on valid_test.py …")
    valid_path = "test_samples/valid_test.py"
    if os.path.exists(valid_path):
        from ml.anomaly_detector import AnomalyDetector
        detector = AnomalyDetector()
        result   = detector.analyse(valid_path)
        print(result.summary())
    else:
        print(f"  File not found: {valid_path}")

    # ── 4. Batch analysis on invalid dataset ──────────────────────────────
    print("\n[Step 4] Batch Analysis — clustering 30 invalid files …")
    batch_dir = "datasets/python/invalid"
    if os.path.isdir(batch_dir):
        # Analyse a small subset to keep the demo fast
        import tempfile, shutil, random
        files = sorted(os.listdir(batch_dir))[:30]
        tmp   = tempfile.mkdtemp()
        for f in files:
            shutil.copy(os.path.join(batch_dir, f), os.path.join(tmp, f))
        from ml.batch_analyzer import BatchAnalyzer
        analyzer = BatchAnalyzer()
        batch    = analyzer.analyse_directory(tmp)
        print(batch.summary())
        shutil.rmtree(tmp)
    else:
        print(f"  Directory not found: {batch_dir}")

    # ── 5. Online learner stats ───────────────────────────────────────────
    print("\n[Step 5] Online Learner Stats …")
    from ml.online_learner import OnlineLearner
    learner = OnlineLearner()
    print(f"  Feedback samples in log: {learner.feedback_count}")
    print(f"  Classes known          : {learner.classes}")
    fsum = learner.feedback_summary()
    if fsum:
        print("  Feedback breakdown:")
        for lbl, cnt in sorted(fsum.items()):
            print(f"    {lbl}: {cnt}")

    print("\n✓ Demo complete.")


# ── CLI dispatcher ────────────────────────────────────────────────────────────

_COMMANDS = {
    'check':    cmd_check,
    'train':    cmd_train,
    'diagnose': cmd_diagnose,
    'batch':    cmd_batch,
    'anomaly':  cmd_anomaly,
    'feedback': cmd_feedback,
    'demo':     cmd_demo,
}

if __name__ == "__main__":
    argv = sys.argv[1:]
    if not argv or argv[0] not in _COMMANDS:
        print(__doc__)
        sys.exit(0)

    cmd  = argv[0]
    rest = argv[1:]

    # Change CWD to project root (the directory containing ml/)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)

    _COMMANDS[cmd](rest)
