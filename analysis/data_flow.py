"""
analysis/data_flow.py — Reaching Definitions & Live Variable Analysis
======================================================================
Implements two classical iterative dataflow analyses over the CFG:

1. REACHING DEFINITIONS (forward):
   - GEN[B]  = variables defined in B (last def wins per var)
   - KILL[B] = all other defs of same variables from other blocks
   - IN[B]   = union of OUT[predecessors]
   - OUT[B]  = GEN[B] ∪ (IN[B] − KILL[B])
   Used to detect: UNDEFINED_NAME (no reaching def), REDUNDANT_ASSIGNMENT

2. LIVE VARIABLE ANALYSIS (backward):
   - USE[B]  = vars read before written in B
   - DEF[B]  = vars written in B
   - OUT[B]  = union of IN[successors]
   - IN[B]   = USE[B] ∪ (OUT[B] − DEF[B])
   Used to detect: UNUSED_VARIABLE (assigned but never live-out)
"""

from __future__ import annotations
from typing import List, Dict, Set, Tuple
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ir.ir_nodes import Op, IRProgram, IRFunction, CFG, BasicBlock


class DFADiagnostic:
    def __init__(self, error_type: str, message: str, line: int,
                 token: str = None, column: int = 0):
        self.error_type = error_type
        self.message    = message
        self.line       = line
        self.column     = column
        self.token      = token


# ─── GEN/KILL/USE/DEF computation ─────────────────────────────────────────────

def _compute_gen_kill(block: BasicBlock) -> Tuple[Set[str], Set[str]]:
    """
    Compute GEN and KILL sets for reaching definitions in one block.
    GEN  = variables first *defined* in this block (set of (var, line) tuples).
    KILL = variable names whose earlier definitions are killed here.
    """
    gen:  Set[Tuple[str, int]] = set()
    kill: Set[str]             = set()
    defined_here: Set[str]     = set()

    for instr in block.instrs:
        if instr.dest and instr.op in (Op.ASSIGN, Op.BINOP, Op.UNOP,
                                        Op.CALL, Op.LOAD, Op.PARAM):
            if instr.dest not in defined_here:
                gen.add((instr.dest, instr.line))
                defined_here.add(instr.dest)
            kill.add(instr.dest)

    return gen, kill


def _compute_use_def(block: BasicBlock) -> Tuple[Set[str], Set[str]]:
    """
    Compute USE and DEF sets for live variable analysis in one block.
    USE = variables read *before* being written in this block.
    DEF = variables written in this block.
    """
    use: Set[str] = set()
    df:  Set[str] = set()

    for instr in block.instrs:
        # First, record reads
        for operand in (instr.arg1, instr.arg2):
            if operand and isinstance(operand, str):
                # Operand is a temp name if it starts with _t, else a source var
                name = operand.split()[0] if operand else None
                if name and not name.startswith(("'", '"', "import(", "iter(",
                                                  "next(", "not_exhausted(",
                                                  "<func", "<class")):
                    if name not in df:
                        use.add(name)
        # Then, record writes
        if instr.dest and instr.op in (Op.ASSIGN, Op.BINOP, Op.UNOP,
                                        Op.CALL, Op.LOAD, Op.PARAM):
            df.add(instr.dest)

    return use, df


# ─── Iterative dataflow solver ─────────────────────────────────────────────────

def reaching_definitions(cfg: CFG) -> Dict[str, Set[Tuple[str, int]]]:
    """
    Compute IN/OUT reaching definition sets for every block.
    Returns dict: block_id → IN set (set of (var_name, def_line) tuples).
    """
    # Initialise
    gen_sets:  Dict[str, Set[Tuple[str, int]]] = {}
    kill_sets: Dict[str, Set[str]]             = {}
    out_sets:  Dict[str, Set[Tuple[str, int]]] = {}

    all_defs: Set[Tuple[str, int]] = set()

    for bid, block in cfg.blocks.items():
        g, k = _compute_gen_kill(block)
        gen_sets[bid]  = g
        kill_sets[bid] = k
        out_sets[bid]  = set(g)
        all_defs.update(g)
        block.gen  = {name for name, _ in g}
        block.kill = k

    in_sets: Dict[str, Set[Tuple[str, int]]] = {bid: set() for bid in cfg.blocks}

    changed = True
    iterations = 0
    while changed and iterations < 100:
        iterations += 1
        changed = False
        for bid in cfg.blocks:
            block = cfg.blocks[bid]
            # IN[B] = union of OUT[pred]
            new_in: Set[Tuple[str, int]] = set()
            for pred in block.predecessors:
                new_in.update(out_sets.get(pred, set()))

            # OUT[B] = GEN[B] ∪ (IN[B] − KILL[B])
            killed_vars = kill_sets[bid]
            filtered_in = {(v, l) for v, l in new_in if v not in killed_vars}
            new_out = gen_sets[bid] | filtered_in

            if new_out != out_sets[bid]:
                out_sets[bid] = new_out
                changed = True

            in_sets[bid] = new_in
            block.in_  = {v for v, _ in new_in}
            block.out_ = {v for v, _ in new_out}

    return in_sets


def live_variable_analysis(cfg: CFG) -> Dict[str, Set[str]]:
    """
    Backward dataflow: compute LIVE_IN/LIVE_OUT for every block.
    Returns dict: block_id → LIVE_IN set.
    """
    use_sets: Dict[str, Set[str]] = {}
    def_sets: Dict[str, Set[str]] = {}
    live_out: Dict[str, Set[str]] = {bid: set() for bid in cfg.blocks}

    for bid, block in cfg.blocks.items():
        u, d = _compute_use_def(block)
        use_sets[bid] = u
        def_sets[bid] = d

    live_in: Dict[str, Set[str]] = {bid: set(use_sets[bid]) for bid in cfg.blocks}

    changed = True
    iterations = 0
    while changed and iterations < 100:
        iterations += 1
        changed = False
        for bid in reversed(list(cfg.blocks.keys())):
            block = cfg.blocks[bid]
            # LIVE_OUT[B] = union of LIVE_IN[successors]
            new_out: Set[str] = set()
            for succ in block.successors:
                new_out.update(live_in.get(succ, set()))

            # LIVE_IN[B] = USE[B] ∪ (LIVE_OUT[B] − DEF[B])
            new_in = use_sets[bid] | (new_out - def_sets[bid])

            if new_in != live_in[bid] or new_out != live_out[bid]:
                live_in[bid]  = new_in
                live_out[bid] = new_out
                changed = True

            block.live_in  = new_in
            block.live_out = new_out

    return live_in


# ─── Diagnostic generation ────────────────────────────────────────────────────

_BUILTINS = {
    'print', 'len', 'range', 'int', 'float', 'str', 'bool', 'list', 'dict',
    'set', 'tuple', 'type', 'isinstance', 'issubclass', 'hasattr', 'getattr',
    'setattr', 'delattr', 'input', 'open', 'format', 'repr', 'abs', 'all',
    'any', 'bin', 'bytes', 'callable', 'chr', 'compile', 'complex', 'dir',
    'divmod', 'enumerate', 'eval', 'exec', 'filter', 'frozenset', 'globals',
    'hash', 'help', 'hex', 'id', 'iter', 'locals', 'map', 'max', 'min',
    'next', 'object', 'oct', 'ord', 'pow', 'property', 'reversed', 'round',
    'slice', 'sorted', 'staticmethod', 'sum', 'super', 'vars', 'zip',
    'True', 'False', 'None', 'Exception', 'ValueError', 'TypeError',
    'KeyError', 'IndexError', 'AttributeError', 'ImportError', 'OSError',
    'RuntimeError', 'StopIteration', 'self', '__name__', '__file__',
}


def _is_temp(name: str) -> bool:
    return name.startswith("_t") and name[2:].isdigit()


def _is_symbol_binding(instr) -> bool:
    return (
        instr.op == Op.ASSIGN
        and isinstance(instr.arg1, str)
        and (instr.arg1.startswith("<func ") or instr.arg1.startswith("<class "))
    )


def analyse_dataflow_for_cfg(name: str, cfg: CFG,
                              params: List[str] = None) -> List[DFADiagnostic]:
    """Run both analyses on one CFG and produce diagnostics."""
    diagnostics: List[DFADiagnostic] = []

    if not cfg.blocks:
        return diagnostics

    reaching_definitions(cfg)
    live_variable_analysis(cfg)

    param_set = set(params or [])

    # ── Collect all definitions: var → (line, block_id) ──────────────────
    all_defs: Dict[str, List[Tuple[int, str]]] = {}
    for bid, block in cfg.blocks.items():
        for instr in block.instrs:
            if (instr.dest and
                    instr.op in (Op.ASSIGN, Op.BINOP, Op.UNOP, Op.CALL, Op.LOAD)
                    and not _is_symbol_binding(instr)
                    and not _is_temp(instr.dest)
                    and instr.dest not in _BUILTINS
                    and instr.dest not in param_set):
                all_defs.setdefault(instr.dest, []).append((instr.line, bid))

    # ── Unused variable: assigned but never live-out in any block ─────────
    all_live: Set[str] = set()
    for block in cfg.blocks.values():
        all_live.update(block.live_in)
        all_live.update(block.live_out)

    for var, defs in all_defs.items():
        if var not in all_live and var not in _BUILTINS and not _is_temp(var):
            first_line = defs[0][0] if defs else 0
            if first_line > 0:
                diagnostics.append(DFADiagnostic(
                    error_type="UNUSED_VARIABLE",
                    message=f"Variable '{var}' is assigned but never used",
                    line=first_line,
                    token=var,
                ))

    # ── Redundant assignment: same var assigned twice with no read between ─
    for bid, block in cfg.blocks.items():
        last_assign: Dict[str, int] = {}  # var → line of last assign
        for instr in block.instrs:
            if (instr.dest and instr.op == Op.ASSIGN
                    and not _is_symbol_binding(instr)
                    and not _is_temp(instr.dest)
                    and instr.dest not in _BUILTINS
                    and instr.dest not in param_set):
                if instr.dest in last_assign and instr.line > 0:
                    diagnostics.append(DFADiagnostic(
                        error_type="REDUNDANT_ASSIGNMENT",
                        message=(f"Variable '{instr.dest}' is assigned again at line "
                                 f"{instr.line} without being read since line "
                                 f"{last_assign[instr.dest]}"),
                        line=instr.line,
                        token=instr.dest,
                    ))
                last_assign[instr.dest] = instr.line
            elif (instr.op == Op.LOAD and instr.arg1 and
                  not _is_temp(instr.arg1 or "")):
                # A read clears the last-assign tracker
                last_assign.pop(instr.arg1, None)

    return diagnostics


def run_data_flow_analysis(ir_program: IRProgram) -> List[DFADiagnostic]:
    """Run data flow analysis on the full IRProgram."""
    results: List[DFADiagnostic] = []
    results.extend(analyse_dataflow_for_cfg("<module>", ir_program.module_cfg))
    for ir_fn in ir_program.functions:
        results.extend(analyse_dataflow_for_cfg(
            ir_fn.name, ir_fn.cfg, params=ir_fn.params))
    return results
