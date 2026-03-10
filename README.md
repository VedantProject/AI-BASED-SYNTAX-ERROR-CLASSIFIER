# AI-Based Syntax Error Classification
## Python Parser & Compiler Analysis Framework

A full-stack compiler front-end and static analysis system for Python. The project implements a complete pipeline from lexing through parsing, AST construction, IR generation, semantic analysis, dataflow analysis, code transformation, and ML-powered error diagnostics — all in pure Python.

---

## Supported Language

| Language | Lexer | Parser |
|----------|-------|--------|
| Python | `lexers/python_lexer.py` | `parsers/python_parser.py` |

---

## Project Structure

```
Parser/
├── grammars/                   # Grammar specification for Python
├── lexers/                     # Python tokenizer
├── parsers/                    # Python recursive-descent parser
├── syntax_tree/                # AST node definitions
├── ir/                         # Intermediate Representation (TAC + CFG)
│   ├── ir_nodes.py             # TAC instruction set, BasicBlock, CFG, IRFunction
│   └── ir_builder.py           # AST → TAC + CFG builder
├── analysis/                   # Static analysis passes
│   ├── control_flow.py         # CFG-based unreachable code, missing return, infinite loop
│   ├── data_flow.py            # Reaching definitions + live-variable analysis
│   ├── pattern_detector.py     # Python AST anti-pattern detection
│   └── runner.py               # Orchestrates all analysis passes
├── ml/                         # Machine learning diagnostics
│   ├── train_classifier.py     # Trains pattern classifier, severity regressor, fix ranker, anomaly detector
│   ├── ast_feature_extractor.py# Extracts 6 feature groups from AST + error context
│   ├── anomaly_detector.py     # Isolation Forest for detecting structurally unusual valid code
│   ├── intelligent_diagnostics.py # Full ML diagnostic engine (classification + severity + fix ranking)
│   ├── batch_analyzer.py       # Directory-level ML analysis with K-Means clustering
│   ├── online_learner.py       # Online learning via user feedback (SGD partial_fit)
│   └── run_ml.py               # ML CLI entry point
├── week_7/                     # 12-stage extended compiler pipeline
│   ├── run_week7.py            # Pipeline entry point
│   ├── core_engine/            # Semantic analyzer (symbol table, scope, types)
│   ├── analysis_modules/       # Control flow, data flow, cyclomatic complexity
│   ├── transformation_modules/ # Constant folding, dead-code elimination, simplification
│   └── ai_or_rules/            # Heuristic rule engine with severity-rated recommendations
├── main/                       # Core controller and utilities
│   ├── controller.py           # ParserController — tokenize → parse → classify
│   ├── error_classifier.py     # Maps error types to categories
│   └── utils.py                # File I/O, JSON output, language detection, reporting
├── datasets/                   # Synthetic valid/invalid Python code samples
├── test_samples/               # Hand-crafted Python test files
├── results/                    # All JSON reports and summaries
├── analyze_code.py             # Standalone CLI syntax error analyzer
├── gui.py                      # Tkinter GUI with dark theme and syntax highlighting
├── demo.py                     # Programmatic demo runner
├── dataset_generator.py        # Synthetic dataset generator
├── main.py                     # Primary CLI entry point
└── requirements.txt
```

---

## Features

### Core Pipeline
- Grammar-driven lexing and recursive-descent parsing for Python
- AST construction with full node definitions
- Three-Address Code (TAC) IR generation with Basic Block and CFG construction
- Batch processing of entire directories

### Static Analysis
- **Control Flow Analysis** — detects unreachable code, missing returns, break/continue outside loops, infinite loops
- **Data Flow Analysis** — reaching definitions (forward) and live-variable analysis (backward); detects undefined names, redundant assignments, unused variables
- **Pattern Detection** — Python-specific AST anti-patterns: mutable default arguments, bare/empty except, `is` literal comparison, builtin shadowing, unused imports

### Code Transformation (Week 7)
- **Constant Folding** — arithmetic constant propagation and strength reduction (`x+0→x`, `x*0→0`, etc.)
- **Dead Code Elimination** — removes unreachable statements after `return`/`break`/`continue` and constant-condition branches
- **Algebraic Simplification** — double-negation, redundant unary+, boolean tautologies, adjacent literal concatenation

### Error Classification
The system classifies Python syntax errors into:
- Missing Delimiter (colons, parentheses, brackets)
- Unmatched Delimiter
- Malformed Expression
- Invalid Declaration / Invalid Type
- Keyword Misuse
- Incomplete Statement
- Indentation Error
- Invalid Import

### Machine Learning Diagnostics
- **Pattern Classifier** — VotingClassifier (Logistic Regression + Random Forest) with calibrated probabilities
- **Severity Regressor** — Ridge regression producing a 0–10 risk score per error
- **Fix Ranker** — Multi-label Logistic Regression ranking top-3 fix actions
- **Anomaly Detector** — Isolation Forest flagging structurally unusual but syntactically valid code
- **Online Learner** — Incremental SGD model updated from user feedback in real time
- **Batch Clustering** — K-Means + PCA clustering to identify systemic coding issues

### Interfaces
- **Primary CLI** (`main.py`) — single-file and batch modes with JSON output option
- **Analyzer CLI** (`analyze_code.py`) — standalone analyzer with interactive, piped, and file-argument modes
- **ML CLI** (`ml/run_ml.py`) — train, diagnose, batch-analyze, anomaly detection, and feedback commands
- **Week 7 Pipeline** (`week_7/run_week7.py`) — full 12-stage compiler pipeline per file
- **GUI** (`gui.py`) — Tkinter desktop application with VS Code-inspired dark theme, syntax highlighting, and threaded analysis

---

## Usage

### Primary CLI

```bash
# Parse a single file
python main.py --file test_samples/valid_test.py

# Output as JSON
python main.py --file test_samples/invalid_test.py --json

# Batch process a directory
python main.py --batch datasets/python/ --output results/

# Verbose output
python main.py --file test_samples/valid_test.py --verbose
```

### Standalone Analyzer

```bash
# Analyze a file
python analyze_code.py test_samples/invalid_test.py

# Interactive paste mode
python analyze_code.py

# Piped input
cat myfile.py | python analyze_code.py
```

### ML Pipeline

```bash
# Check if models are trained
python -m ml.run_ml check

# Train all models
python -m ml.run_ml train

# Diagnose a file
python -m ml.run_ml diagnose test_samples/invalid_test.py

# Batch analysis with clustering
python -m ml.run_ml batch datasets/python/

# Anomaly detection
python -m ml.run_ml anomaly test_samples/valid_test.py

# Submit user feedback to online learner
python -m ml.run_ml feedback test_samples/invalid_test.py correct_label

# Run demo
python -m ml.run_ml demo
```

### Week 7 — 12-Stage Compiler Pipeline

```bash
python week_7/run_week7.py --file test_samples/valid_test.py
python week_7/run_week7.py --file test_samples/invalid_test.py --verbose
```

**Pipeline stages:**

| Stage | Description |
|-------|-------------|
| 0 | Source loading |
| 1 | Lexical analysis |
| 2 | Syntax / parse analysis |
| 3 | AST serialization |
| 4 | Semantic analysis (symbol table, scope, type consistency) |
| 5 | Control flow analysis |
| 6 | Data flow analysis |
| 7 | Complexity metrics (cyclomatic complexity, nesting depth, LOC) |
| 8 | Constant folding |
| 9 | Dead code elimination |
| 10 | Algebraic simplification |
| 11 | Heuristic rule engine (severity-rated recommendations) |
| 12 | Report generation (JSON + flat text log) |

### Dataset Generation & Demo

```bash
# Generate synthetic datasets
python dataset_generator.py --language python --count 500

# Run programmatic demo
python demo.py

# Launch GUI
python gui.py
```

---

## Output Format

Each analysis produces structured JSON. Example diagnostic:

```json
{
  "language": "Python",
  "error_type": "IndentationError",
  "line": 6,
  "message": "Unexpected indentation block",
  "severity": 7.2,
  "suggested_fixes": [
    "Check indentation consistency",
    "Ensure block is inside a function or loop"
  ]
}
```

Week 7 pipeline outputs a JSON file per stage under `results/week_7_outputs/` and full pipeline logs under `results/week_7_logs/`.

---

## Requirements

- Python 3.8+
- `colorama`, `tabulate` — colored/formatted terminal output
- `scikit-learn >= 1.3.0`, `numpy >= 1.24.0` — ML features (optional)

```bash
pip install -r requirements.txt
```

---

## Results

Pre-computed results are stored in `results/`:

| Directory | Contents |
|-----------|----------|
| `batch_c/`, `batch_java/`, `batch_python/` | Batch parse results and summaries |
| `demo/` | Demo run outputs |
| `final/` | Consolidated final report |
| `ml_anomaly/` | Per-file anomaly detection reports |
| `ml_diagnostics/` | Per-file intelligent diagnostics reports |
| `week_7_outputs/` | 12 stage-level JSON files per input file |
| `week_7_logs/` | Structured pipeline logs |
