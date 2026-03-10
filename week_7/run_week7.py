"""
Week 7 · Main Runner
====================
End-to-end pipeline that extends the existing Multi-Language Parser Framework
with all Week 7 compiler passes.

Pipeline stages
---------------
  Stage 0 – Source loading
  Stage 1 – Lexical analysis          (reuses existing lexers/)
  Stage 2 – Syntax / parse analysis   (reuses existing parsers/)
  Stage 3 – AST serialisation         (reuses existing syntax_tree.ast_to_dict)
  Stage 4 – Semantic analysis         (week_7/core_engine/semantic_analyzer.py)
  Stage 5 – Control-flow analysis     (week_7/analysis_modules/control_flow.py)
  Stage 6 – Data-flow analysis        (week_7/analysis_modules/data_flow.py)
  Stage 7 – Complexity analysis       (week_7/analysis_modules/complexity.py)
  Stage 8 – Constant folding          (week_7/transformation_modules/constant_folder.py)
  Stage 9 – Dead-code elimination     (week_7/transformation_modules/dead_code_eliminator.py)
  Stage 10– Code simplification       (week_7/transformation_modules/simplifier.py)
  Stage 11– Rule / heuristic engine   (week_7/ai_or_rules/rule_engine.py)
  Stage 12– Report generation

Outputs
-------
  results/week_7_outputs/<basename>_<stage>.json   – intermediate JSON per stage
  results/week_7_logs/<basename>_pipeline.log      – flat text log
  results/week_7_logs/<basename>_pipeline.json     – structured JSON log

Usage
-----
  python week_7/run_week7.py --file test_samples/valid_test.c
  python week_7/run_week7.py --file test_samples/invalid_test.py --language python
  python week_7/run_week7.py --file test_samples/ValidTest.java --verbose
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ── path setup: make sure the project root is importable ─────────────────────
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

# ── Existing project components ───────────────────────────────────────────────
from lexers import tokenize_c, tokenize_java, tokenize_python
from parsers import parse_c, parse_java, parse_python
from syntax_tree.ast_nodes import ast_to_dict, Program
from main.utils import read_file, write_json, get_language_from_extension, ensure_dir

# ── Week 7 components ─────────────────────────────────────────────────────────
from week_7.core_engine.semantic_analyzer import SemanticAnalyzer
from week_7.analysis_modules.control_flow  import ControlFlowAnalyzer
from week_7.analysis_modules.data_flow     import DataFlowAnalyzer
from week_7.analysis_modules.complexity    import ComplexityAnalyzer
from week_7.transformation_modules.constant_folder    import ConstantFolder
from week_7.transformation_modules.dead_code_eliminator import DeadCodeEliminator
from week_7.transformation_modules.simplifier         import CodeSimplifier
from week_7.ai_or_rules.rule_engine import RuleEngine, RuleContext


# ══════════════════════════════════════════════════════════════════════════════
# Logger
# ══════════════════════════════════════════════════════════════════════════════

class PipelineLogger:
    """Lightweight dual-output logger (console + in-memory log list)."""

    def __init__(self, verbose: bool = False):
        self.verbose  = verbose
        self.entries: List[Dict] = []

    def _entry(self, level: str, stage: str, message: str) -> Dict:
        e = {"timestamp": datetime.now().isoformat(),
             "level": level, "stage": stage, "message": message}
        self.entries.append(e)
        return e

    def info(self, stage: str, message: str):
        e = self._entry("INFO", stage, message)
        print(f"  [INFO]  [{stage}] {message}")

    def warn(self, stage: str, message: str):
        e = self._entry("WARN", stage, message)
        print(f"  [WARN]  [{stage}] {message}")

    def error(self, stage: str, message: str):
        e = self._entry("ERROR", stage, message)
        print(f"  [ERROR] [{stage}] {message}")

    def phase(self, name: str):
        line = f"\n{'─'*60}\n  ▶  {name}\n{'─'*60}"
        self._entry("PHASE", name, "START")
        print(line)

    def phase_done(self, name: str, elapsed: float):
        msg = f"✓  {name}  ({elapsed*1000:.1f} ms)"
        self._entry("PHASE_DONE", name, msg)
        print(f"  {msg}")

    def save(self, log_dir: str, basename: str):
        ensure_dir(log_dir)
        # Structured JSON log
        json_path = os.path.join(log_dir, f"{basename}_pipeline.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self.entries, f, indent=2)
        # Flat text log
        txt_path = os.path.join(log_dir, f"{basename}_pipeline.log")
        with open(txt_path, "w", encoding="utf-8") as f:
            for e in self.entries:
                f.write(f"[{e['timestamp']}] [{e['level']}] [{e['stage']}] {e['message']}\n")
        return json_path, txt_path


# ══════════════════════════════════════════════════════════════════════════════
# Pipeline
# ══════════════════════════════════════════════════════════════════════════════

class Week7Pipeline:
    """
    Orchestrates all pipeline stages.

    Parameters
    ----------
    out_dir : str  – path where intermediate JSON outputs are written
    log_dir : str  – path where log files are written
    verbose : bool – enable verbose console output
    """

    _TOKENIZERS = {"c": tokenize_c, "java": tokenize_java, "python": tokenize_python}
    _PARSERS    = {"c": parse_c,    "java": parse_java,    "python": parse_python}

    def __init__(self, out_dir: str = "results/week_7_outputs",
                 log_dir: str = "results/week_7_logs",
                 verbose: bool = False):
        self.out_dir = out_dir
        self.log_dir = log_dir
        self.verbose = verbose
        self.logger  = PipelineLogger(verbose)
        ensure_dir(out_dir)
        ensure_dir(log_dir)

    # ── public entry point ────────────────────────────────────────────────────

    def run(self, filepath: str, language: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute the full Week 7 pipeline for *filepath*.

        Returns a JSON-serialisable summary dict.
        """
        start_total = time.perf_counter()

        basename = Path(filepath).stem
        lang     = language or get_language_from_extension(filepath)

        print(f"\n{'═'*60}")
        print(f"  WEEK 7 COMPILER PIPELINE")
        print(f"  File     : {filepath}")
        print(f"  Language : {lang}")
        print(f"  Started  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'═'*60}")

        pipeline_result: Dict[str, Any] = {
            "file":      filepath,
            "language":  lang,
            "timestamp": datetime.now().isoformat(),
            "stages":    {},
            "status":    "running",
        }

        try:
            # ── Stage 0: Source loading ────────────────────────────────────
            source_code = self._stage_load(filepath, pipeline_result)

            # ── Stage 1: Lexical analysis ──────────────────────────────────
            tokens = self._stage_lex(source_code, lang, basename, pipeline_result)

            # ── Stage 2: Parse / syntax analysis ──────────────────────────
            ast_root, parse_errors = self._stage_parse(tokens, lang, basename, pipeline_result)

            # ── Stage 3: AST serialisation ─────────────────────────────────
            ast_dict = self._stage_ast_serialise(ast_root, basename, pipeline_result)

            # ── Stage 4: Semantic analysis ─────────────────────────────────
            semantic = self._stage_semantic(ast_root, lang, basename, pipeline_result)

            # ── Stage 5: Control-flow analysis ────────────────────────────
            cfa = self._stage_control_flow(ast_root, basename, pipeline_result)

            # ── Stage 6: Data-flow analysis ────────────────────────────────
            dfa = self._stage_data_flow(ast_root, basename, pipeline_result)

            # ── Stage 7: Complexity analysis ───────────────────────────────
            complexity = self._stage_complexity(ast_root, basename, pipeline_result)

            # ── Stage 8: Constant folding ──────────────────────────────────
            ast_root, fold_log = self._stage_constant_fold(ast_root, basename, pipeline_result)

            # ── Stage 9: Dead-code elimination ────────────────────────────
            ast_root, dce_log = self._stage_dead_code(ast_root, basename, pipeline_result)

            # ── Stage 10: Code simplification ─────────────────────────────
            ast_root, simp_log = self._stage_simplify(ast_root, basename, pipeline_result)

            # Combined transformation log
            combined_transform_log = fold_log + dce_log + simp_log
            pipeline_result["stages"]["transformations"] = {
                "constant_fold_changes": len(fold_log),
                "dead_code_eliminations": len(dce_log),
                "simplifications":        len(simp_log),
                "total_changes":          len(combined_transform_log),
            }

            # Save the final transformed AST
            final_ast_dict = ast_to_dict(ast_root) if ast_root else {}
            self._save_output(final_ast_dict, basename, "final_ast")

            # ── Stage 11: Rule / heuristic engine ─────────────────────────
            rule_result = self._stage_rules(
                lang, filepath, source_code,
                semantic, cfa, dfa, complexity,
                combined_transform_log,
                basename, pipeline_result
            )

            # ── Stage 12: Final report ─────────────────────────────────────
            elapsed_total = time.perf_counter() - start_total
            pipeline_result["status"]        = "success"
            pipeline_result["elapsed_ms"]    = round(elapsed_total * 1000, 2)
            pipeline_result["overall_grade"] = rule_result.get("overall_grade", "?")

            self._save_output(pipeline_result, basename, "pipeline_summary")
            log_json, log_txt = self.logger.save(self.log_dir, basename)

            self._print_summary(pipeline_result, rule_result, log_json, log_txt)

        except Exception as exc:
            elapsed_total = time.perf_counter() - start_total
            pipeline_result["status"]     = "failed"
            pipeline_result["error"]      = str(exc)
            pipeline_result["traceback"]  = traceback.format_exc()
            pipeline_result["elapsed_ms"] = round(elapsed_total * 1000, 2)
            self.logger.error("Pipeline", f"Fatal: {exc}")
            self.logger.save(self.log_dir, basename)
            print(f"\n  [FATAL] Pipeline failed: {exc}")
            traceback.print_exc()

        return pipeline_result

    # ══════════════════════════════════════════════════════════════════════════
    # Individual stage methods
    # ══════════════════════════════════════════════════════════════════════════

    def _stage_load(self, filepath: str, result: Dict) -> str:
        self.logger.phase("Stage 0 · Source Loading")
        t = time.perf_counter()
        source = read_file(filepath)
        elapsed = time.perf_counter() - t
        lines = source.count("\n") + 1
        self.logger.info("Load", f"{lines} lines, {len(source)} bytes")
        result["stages"]["load"] = {"lines": lines, "bytes": len(source)}
        self.logger.phase_done("Source Loading", elapsed)
        return source

    def _stage_lex(self, source: str, lang: str, base: str, result: Dict):
        self.logger.phase("Stage 1 · Lexical Analysis")
        t = time.perf_counter()
        tokenizer = self._TOKENIZERS.get(lang)
        if tokenizer is None:
            raise ValueError(f"Unsupported language: '{lang}'")
        tokens = tokenizer(source)
        elapsed = time.perf_counter() - t

        token_data = [{"type": tok.type, "value": tok.value,
                       "line": tok.line, "column": tok.column}
                      for tok in tokens]
        self._save_output(token_data, base, "1_tokens")

        # Summary by token type
        type_counts: Dict[str, int] = {}
        for tok in tokens:
            type_counts[tok.type] = type_counts.get(tok.type, 0) + 1

        self.logger.info("Lexer", f"{len(tokens)} tokens, {len(type_counts)} distinct types")
        result["stages"]["lexer"] = {
            "token_count": len(tokens),
            "distinct_types": len(type_counts),
            "type_distribution": type_counts,
        }
        self.logger.phase_done("Lexical Analysis", elapsed)
        return tokens

    def _stage_parse(self, tokens, lang: str, base: str, result: Dict):
        self.logger.phase("Stage 2 · Syntax / Parse Analysis")
        t = time.perf_counter()
        parser_fn = self._PARSERS.get(lang)
        if parser_fn is None:
            raise ValueError(f"No parser for language: '{lang}'")
        ast_root, errors = parser_fn(tokens)
        elapsed = time.perf_counter() - t

        error_list = [{"type": e.error_type, "message": e.message,
                       "line": e.line, "column": e.column}
                      for e in errors]
        self._save_output(error_list, base, "2_parse_errors")

        self.logger.info("Parser", f"{len(errors)} syntax error(s)")
        if errors:
            for e in errors[:3]:
                self.logger.warn("Parser", f"  Line {e.line}: {e.message}")
            if len(errors) > 3:
                self.logger.warn("Parser", f"  … and {len(errors)-3} more")

        result["stages"]["parser"] = {
            "syntax_error_count": len(errors),
            "parse_success":      len(errors) == 0,
        }
        self.logger.phase_done("Syntax Analysis", elapsed)
        return ast_root, errors

    def _stage_ast_serialise(self, ast_root, base: str, result: Dict) -> Dict:
        self.logger.phase("Stage 3 · AST Serialisation")
        t = time.perf_counter()
        ast_dict = ast_to_dict(ast_root) if ast_root else {}
        self._save_output(ast_dict, base, "3_ast")
        elapsed = time.perf_counter() - t
        node_count = self._count_nodes(ast_dict)
        self.logger.info("AST", f"{node_count} nodes serialised")
        result["stages"]["ast_serialise"] = {"node_count": node_count}
        self.logger.phase_done("AST Serialisation", elapsed)
        return ast_dict

    def _stage_semantic(self, ast_root, lang: str, base: str, result: Dict) -> Dict:
        self.logger.phase("Stage 4 · Semantic Analysis")
        t = time.perf_counter()
        sem = SemanticAnalyzer(language=lang)
        sem_result = sem.analyze(ast_root) if ast_root else {}
        self._save_output(sem_result, base, "4_semantic")
        elapsed = time.perf_counter() - t

        stats = sem_result.get("statistics", {})
        self.logger.info("Semantic", f"{stats.get('total_symbols',0)} symbols, "
                                     f"{stats.get('semantic_errors',0)} errors, "
                                     f"{stats.get('semantic_warnings',0)} warnings")
        result["stages"]["semantic"] = stats
        self.logger.phase_done("Semantic Analysis", elapsed)
        return sem_result

    def _stage_control_flow(self, ast_root, base: str, result: Dict) -> Dict:
        self.logger.phase("Stage 5 · Control-Flow Analysis")
        t = time.perf_counter()
        cfa = ControlFlowAnalyzer()
        cfa_result = cfa.analyze(ast_root) if ast_root else {}
        self._save_output(cfa_result, base, "5_control_flow")
        elapsed = time.perf_counter() - t

        s = cfa_result.get("summary", {})
        self.logger.info("CFG", f"{s.get('total_blocks',0)} blocks, "
                                f"{s.get('total_edges',0)} edges, "
                                f"{s.get('loops_detected',0)} loop(s), "
                                f"{s.get('unreachable_blocks',0)} unreachable")
        result["stages"]["control_flow"] = s
        self.logger.phase_done("Control-Flow Analysis", elapsed)
        return cfa_result

    def _stage_data_flow(self, ast_root, base: str, result: Dict) -> Dict:
        self.logger.phase("Stage 6 · Data-Flow Analysis")
        t = time.perf_counter()
        dfa = DataFlowAnalyzer()
        dfa_result = dfa.analyze(ast_root) if ast_root else {}
        self._save_output(dfa_result, base, "6_data_flow")
        elapsed = time.perf_counter() - t

        s = dfa_result.get("summary", {})
        self.logger.info("DFA", f"{s.get('total_definitions',0)} defs, "
                                f"{s.get('total_uses',0)} uses, "
                                f"{s.get('uninitialized_count',0)} uninitialised, "
                                f"{s.get('dead_definition_count',0)} dead defs")
        result["stages"]["data_flow"] = s
        self.logger.phase_done("Data-Flow Analysis", elapsed)
        return dfa_result

    def _stage_complexity(self, ast_root, base: str, result: Dict) -> Dict:
        self.logger.phase("Stage 7 · Complexity Analysis")
        t = time.perf_counter()
        ca = ComplexityAnalyzer()
        ca_result = ca.analyze(ast_root) if ast_root else {}
        self._save_output(ca_result, base, "7_complexity")
        elapsed = time.perf_counter() - t

        self.logger.info("Complexity", f"CC={ca_result.get('cyclomatic_complexity','?')}, "
                                       f"depth={ca_result.get('max_nesting_depth','?')}, "
                                       f"rating={ca_result.get('complexity_rating','?')}, "
                                       f"LOC≈{ca_result.get('estimated_loc','?')}")
        result["stages"]["complexity"] = {
            k: ca_result[k] for k in
            ("cyclomatic_complexity", "max_nesting_depth", "statement_count",
             "function_count", "estimated_loc", "complexity_rating")
            if k in ca_result
        }
        self.logger.phase_done("Complexity Analysis", elapsed)
        return ca_result

    def _stage_constant_fold(self, ast_root, base: str, result: Dict):
        self.logger.phase("Stage 8 · Constant Folding")
        t = time.perf_counter()
        folder = ConstantFolder()
        new_ast, log = folder.transform(ast_root) if ast_root else (ast_root, [])
        self._save_output(log, base, "8_constant_fold_log")
        elapsed = time.perf_counter() - t
        self.logger.info("ConstFold", f"{len(log)} fold(s) applied")
        result["stages"]["constant_folding"] = {"changes": len(log)}
        self.logger.phase_done("Constant Folding", elapsed)
        return new_ast, log

    def _stage_dead_code(self, ast_root, base: str, result: Dict):
        self.logger.phase("Stage 9 · Dead-Code Elimination")
        t = time.perf_counter()
        dce = DeadCodeEliminator()
        new_ast, log = dce.transform(ast_root) if ast_root else (ast_root, [])
        self._save_output(log, base, "9_dead_code_log")
        elapsed = time.perf_counter() - t
        self.logger.info("DCE", f"{len(log)} elimination(s) applied")
        result["stages"]["dead_code_elimination"] = {"eliminations": len(log)}
        self.logger.phase_done("Dead-Code Elimination", elapsed)
        return new_ast, log

    def _stage_simplify(self, ast_root, base: str, result: Dict):
        self.logger.phase("Stage 10 · Code Simplification")
        t = time.perf_counter()
        simp = CodeSimplifier()
        new_ast, log = simp.transform(ast_root) if ast_root else (ast_root, [])
        self._save_output(log, base, "10_simplify_log")
        elapsed = time.perf_counter() - t
        self.logger.info("Simplifier", f"{len(log)} simplification(s) applied")
        result["stages"]["simplification"] = {"changes": len(log)}
        self.logger.phase_done("Code Simplification", elapsed)
        return new_ast, log

    def _stage_rules(self, lang, filepath, source_code,
                     semantic, cfa, dfa, complexity,
                     transform_log, base, result) -> Dict:
        self.logger.phase("Stage 11 · Rule / Heuristic Engine")
        t = time.perf_counter()

        ctx = RuleContext(
            language           = lang,
            filename           = filepath,
            source_code        = source_code,
            semantic           = semantic,
            control_flow       = cfa,
            data_flow          = dfa,
            complexity         = complexity,
            transformation_log = transform_log,
        )
        engine = RuleEngine()
        rule_result = engine.process(ctx)
        self._save_output(rule_result, base, "11_rule_engine")
        elapsed = time.perf_counter() - t

        s = rule_result["summary"]
        self.logger.info("Rules", f"{s['rules_fired']}/{s['total_rules_evaluated']} rules fired  "
                                  f"– {s['errors']} error(s), {s['warnings']} warning(s), "
                                  f"grade: {s['grade']}")
        result["stages"]["rule_engine"] = rule_result["summary"]
        self.logger.phase_done("Rule Engine", elapsed)
        return rule_result

    # ── utilities ─────────────────────────────────────────────────────────────

    def _save_output(self, data: Any, basename: str, stage_suffix: str) -> str:
        filename = f"{basename}_{stage_suffix}.json"
        path = os.path.join(self.out_dir, filename)
        write_json(path, data)
        self.logger.info("Output", f"Saved → {path}")
        return path

    @staticmethod
    def _count_nodes(d: Any, count: int = 0) -> int:
        if isinstance(d, dict):
            count += 1
            for v in d.values():
                count = Week7Pipeline._count_nodes(v, count)
        elif isinstance(d, list):
            for item in d:
                count = Week7Pipeline._count_nodes(item, count)
        return count

    # ── summary printer ───────────────────────────────────────────────────────

    def _print_summary(self, pipeline_result: Dict, rule_result: Dict,
                       log_json: str, log_txt: str):
        grade = pipeline_result.get("overall_grade", "?")
        elapsed = pipeline_result.get("elapsed_ms", 0)

        grade_colour = ""

        print(f"\n{'═'*60}")
        print(f"  WEEK 7 PIPELINE COMPLETE  –  Grade: {grade}")
        print(f"  Total time: {elapsed:.1f} ms")
        print(f"{'─'*60}")

        stages = pipeline_result.get("stages", {})

        def _row(label, value):
            print(f"  {label:<30} {value}")

        if "load" in stages:
            _row("Source lines:", stages["load"].get("lines", "?"))
        if "lexer" in stages:
            _row("Tokens:", stages["lexer"].get("token_count", "?"))
        if "parser" in stages:
            _row("Syntax errors:", stages["parser"].get("syntax_error_count", "?"))
        if "semantic" in stages:
            _row("Symbols:",        stages["semantic"].get("total_symbols", "?"))
            _row("Semantic errors:", stages["semantic"].get("semantic_errors", "?"))
        if "control_flow" in stages:
            _row("CFG blocks:",      stages["control_flow"].get("total_blocks", "?"))
            _row("Loops detected:",  stages["control_flow"].get("loops_detected", "?"))
        if "data_flow" in stages:
            _row("Uninitialised vars:", stages["data_flow"].get("uninitialized_count", "?"))
            _row("Dead definitions:",   stages["data_flow"].get("dead_definition_count", "?"))
        if "complexity" in stages:
            _row("Cyclomatic complexity:", stages["complexity"].get("cyclomatic_complexity", "?"))
            _row("Max nesting depth:",     stages["complexity"].get("max_nesting_depth", "?"))
            _row("Complexity rating:",     stages["complexity"].get("complexity_rating", "?"))
        if "transformations" in stages:
            _row("Transformations applied:", stages["transformations"].get("total_changes", "?"))

        print(f"{'─'*60}")
        rs = rule_result.get("summary", {})
        _row("Rules fired:",    f"{rs.get('rules_fired','?')} / {rs.get('total_rules_evaluated','?')}")
        _row("Errors:",         rs.get("errors", "?"))
        _row("Warnings:",       rs.get("warnings", "?"))
        _row("Overall grade:",  grade)

        # Print recommendations
        recs = rule_result.get("recommendations", [])
        if recs:
            print(f"{'─'*60}")
            print("  Recommendations:")
            for i, rec in enumerate(recs, 1):
                # Wrap long lines
                words = rec.split()
                line, col_count = "    " + str(i) + ". ", 0
                for w in words:
                    if col_count + len(w) > 70:
                        print(line)
                        line = "       "
                        col_count = 0
                    line += w + " "
                    col_count += len(w) + 1
                print(line)

        print(f"{'─'*60}")
        print(f"  Outputs : {self.out_dir}/")
        print(f"  Logs    : {log_txt}")
        print(f"            {log_json}")
        print(f"{'═'*60}\n")


# ══════════════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════════════

def build_arg_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="run_week7",
        description="Week 7 Extended Compiler Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python week_7/run_week7.py --file test_samples/valid_test.c
  python week_7/run_week7.py --file test_samples/invalid_test.py --language python
  python week_7/run_week7.py --file test_samples/ValidTest.java --verbose
  python week_7/run_week7.py --file test_samples/valid_test.c \\
         --out-dir results/my_run/outputs --log-dir results/my_run/logs
        """,
    )
    ap.add_argument("--file",     "-f", required=True,
                    help="Path to source file (.c / .java / .py)")
    ap.add_argument("--language", "-l", choices=["c", "java", "python"],
                    help="Override language detection")
    ap.add_argument("--out-dir",  default="results/week_7_outputs",
                    help="Directory for intermediate JSON outputs (default: results/week_7_outputs)")
    ap.add_argument("--log-dir",  default="results/week_7_logs",
                    help="Directory for log files (default: results/week_7_logs)")
    ap.add_argument("--verbose",  "-v", action="store_true",
                    help="Enable verbose output")
    return ap


def main():
    ap = build_arg_parser()
    args = ap.parse_args()

    pipeline = Week7Pipeline(
        out_dir = args.out_dir,
        log_dir = args.log_dir,
        verbose = args.verbose,
    )

    result = pipeline.run(args.file, language=args.language)

    # Exit with non-zero if pipeline itself failed
    sys.exit(0 if result.get("status") == "success" else 1)


if __name__ == "__main__":
    main()
