"""
ir/ir_nodes.py — Intermediate Representation Data Model
=========================================================
Defines Three-Address Code (TAC) instructions and the Control Flow Graph (CFG).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Set, Dict


# ─── TAC Instruction opcodes ──────────────────────────────────────────────────

class Op:
    ASSIGN  = "ASSIGN"    # dest = arg1
    BINOP   = "BINOP"     # dest = arg1 op arg2
    UNOP    = "UNOP"      # dest = op arg1
    CALL    = "CALL"      # dest = CALL name(args...)
    RETURN  = "RETURN"    # RETURN arg1  (arg1 may be None)
    JUMP    = "JUMP"      # JUMP label
    CJUMP   = "CJUMP"     # CJUMP cond true_label false_label
    LABEL   = "LABEL"     # LABEL name
    PARAM   = "PARAM"     # PARAM arg1  (push argument)
    LOAD    = "LOAD"      # dest = LOAD name  (load from name)
    NOP     = "NOP"       # no-op / placeholder


@dataclass
class TACInstr:
    """One Three-Address Code instruction."""
    op:     str
    dest:   Optional[str] = None   # destination temp/var
    arg1:   Optional[str] = None   # first operand or function name
    arg2:   Optional[str] = None   # second operand or operator symbol
    label:  Optional[str] = None   # jump target label
    line:   int = 0                # source line number

    def __str__(self) -> str:
        if self.op == Op.ASSIGN:
            return f"{self.dest} = {self.arg1}"
        if self.op == Op.BINOP:
            return f"{self.dest} = {self.arg1} {self.arg2} ???"  # arg2 is op, filled by builder
        if self.op == Op.UNOP:
            return f"{self.dest} = {self.arg2}{self.arg1}"
        if self.op == Op.CALL:
            return f"{self.dest} = CALL {self.arg1}({self.arg2 or ''})"
        if self.op == Op.RETURN:
            return f"RETURN {self.arg1 or ''}"
        if self.op == Op.JUMP:
            return f"JUMP {self.label}"
        if self.op == Op.CJUMP:
            return f"CJUMP {self.arg1} → {self.label} / {self.arg2}"
        if self.op == Op.LABEL:
            return f"LABEL {self.label}:"
        if self.op == Op.PARAM:
            return f"PARAM {self.arg1}"
        if self.op == Op.LOAD:
            return f"{self.dest} = {self.arg1}"
        return f"NOP"


# ─── Basic Block ──────────────────────────────────────────────────────────────

@dataclass
class BasicBlock:
    """A maximal straight-line sequence of TAC instructions."""
    id:           str
    instrs:       List[TACInstr]          = field(default_factory=list)
    successors:   List[str]               = field(default_factory=list)  # block IDs
    predecessors: List[str]               = field(default_factory=list)
    # Dataflow sets (populated by data_flow.py)
    gen:          Set[str]                = field(default_factory=set)
    kill:         Set[str]                = field(default_factory=set)
    in_:          Set[str]                = field(default_factory=set)
    out_:         Set[str]                = field(default_factory=set)
    live_in:      Set[str]                = field(default_factory=set)
    live_out:     Set[str]                = field(default_factory=set)

    def __repr__(self) -> str:
        return f"BB({self.id}, {len(self.instrs)} instrs)"


# ─── Control Flow Graph ───────────────────────────────────────────────────────

@dataclass
class CFG:
    """Control Flow Graph for one function (or the module top-level)."""
    entry:  str                       = "entry"
    exit:   str                       = "exit"
    blocks: Dict[str, BasicBlock]     = field(default_factory=dict)

    def add_block(self, block: BasicBlock):
        self.blocks[block.id] = block

    def link(self, from_id: str, to_id: str):
        """Add an edge from_id → to_id."""
        if from_id in self.blocks and to_id in self.blocks:
            if to_id not in self.blocks[from_id].successors:
                self.blocks[from_id].successors.append(to_id)
            if from_id not in self.blocks[to_id].predecessors:
                self.blocks[to_id].predecessors.append(from_id)

    def reachable_from_entry(self) -> Set[str]:
        """Return set of block IDs reachable from the entry block."""
        visited: Set[str] = set()
        stack = [self.entry]
        while stack:
            bid = stack.pop()
            if bid in visited or bid not in self.blocks:
                continue
            visited.add(bid)
            stack.extend(self.blocks[bid].successors)
        return visited


# ─── IR Function / Program ────────────────────────────────────────────────────

@dataclass
class IRFunction:
    """IR representation of one Python function or class method."""
    name:       str
    params:     List[str]   = field(default_factory=list)
    cfg:        CFG         = field(default_factory=CFG)
    line:       int         = 0

    def all_instrs(self) -> List[TACInstr]:
        result = []
        for block in self.cfg.blocks.values():
            result.extend(block.instrs)
        return result


@dataclass
class IRProgram:
    """Top-level IR: module-level CFG + all function IRs."""
    module_cfg:  CFG                    = field(default_factory=CFG)
    functions:   List[IRFunction]       = field(default_factory=list)

    def all_cfgs(self) -> List[tuple]:
        """Return list of (name, CFG) for module + all functions."""
        result = [("<module>", self.module_cfg)]
        for fn in self.functions:
            result.append((fn.name, fn.cfg))
        return result
