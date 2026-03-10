"""
Week 7 · Analysis Modules → Control-Flow Analyser
===================================================
Builds a Control-Flow Graph (CFG) from the real AST nodes produced by the
existing parsers and computes:

  • Basic blocks    – maximal straight-line instruction sequences
  • CFG edges       – (from_id, to_id, edge_type) triples
  • Loop detection  – back-edges in the graph
  • Branch count    – number of if / switch decision points
  • Unreachable blocks – blocks not reachable from entry

The analyser is read-only; the AST is never mutated.

Public API
----------
    cfa = ControlFlowAnalyzer()
    result = cfa.analyze(ast_program_node)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set

from syntax_tree.ast_nodes import (
    ASTNode, Program, Block,
    FunctionDecl, ClassDecl,
    IfStmt, WhileStmt, ForStmt,
    ReturnStmt, BreakStmt, ContinueStmt,
    ExpressionStmt, VariableDecl,
)


# ══════════════════════════════════════════════════════════════════════════════
# Data structures
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class BasicBlock:
    """A maximal sequence of straight-line statements."""
    block_id:   int
    label:      str = ""
    stmts:      List[str]  = field(default_factory=list)   # textual summaries
    stmt_lines: List[int]  = field(default_factory=list)   # source lines
    is_entry:   bool = False
    is_exit:    bool = False

    def to_dict(self) -> Dict:
        return {
            "block_id":   self.block_id,
            "label":      self.label,
            "stmts":      self.stmts,
            "stmt_lines": self.stmt_lines,
            "is_entry":   self.is_entry,
            "is_exit":    self.is_exit,
        }


@dataclass
class CFGEdge:
    """Directed edge in the control-flow graph."""
    from_id:   int
    to_id:     int
    edge_type: str = "sequential"   # sequential | true_branch | false_branch
                                    # loop_back   | exception

    def to_dict(self) -> Dict:
        return {"from": self.from_id, "to": self.to_id, "type": self.edge_type}


# ══════════════════════════════════════════════════════════════════════════════
# Control-Flow Analyser
# ══════════════════════════════════════════════════════════════════════════════

class ControlFlowAnalyzer:
    """Builds and analyses a CFG from an AST."""

    def __init__(self):
        self._blocks: List[BasicBlock] = []
        self._edges:  List[CFGEdge]   = []
        self._next_id = 0

    # ── public entry point ────────────────────────────────────────────────────

    def analyze(self, root: ASTNode) -> Dict[str, Any]:
        """
        Analyse the AST and return a JSON-serialisable result dict with keys:
          blocks, edges, loops, branch_count, unreachable_block_ids, summary
        """
        self._blocks  = []
        self._edges   = []
        self._next_id = 0

        # Entry sentinel
        entry = self._new_block("ENTRY", is_entry=True)
        last_id = self._visit(root, entry.block_id)

        # Exit sentinel
        exit_block = self._new_block("EXIT", is_exit=True)
        if last_id is not None:
            self._add_edge(last_id, exit_block.block_id, "sequential")

        # Compute derived information
        loops       = self._find_loops()
        branches    = sum(1 for b in self._blocks if "IF" in b.label or "LOOP" in b.label)
        unreachable = self._find_unreachable()

        return {
            "blocks":              [b.to_dict() for b in self._blocks],
            "edges":               [e.to_dict() for e in self._edges],
            "loops":               loops,
            "branch_count":        branches,
            "unreachable_block_ids": unreachable,
            "summary": {
                "total_blocks":      len(self._blocks),
                "total_edges":       len(self._edges),
                "loops_detected":    len(loops),
                "branches_detected": branches,
                "unreachable_blocks": len(unreachable),
            },
        }

    # ── internal block/edge helpers ───────────────────────────────────────────

    def _new_block(self, label: str = "", is_entry=False, is_exit=False) -> BasicBlock:
        b = BasicBlock(block_id=self._next_id, label=label,
                       is_entry=is_entry, is_exit=is_exit)
        self._next_id += 1
        self._blocks.append(b)
        return b

    def _add_edge(self, from_id: int, to_id: int, edge_type: str = "sequential"):
        # Avoid duplicate edges
        for e in self._edges:
            if e.from_id == from_id and e.to_id == to_id:
                return
        self._edges.append(CFGEdge(from_id, to_id, edge_type))

    def _stmt_summary(self, node: ASTNode) -> str:
        """One-line textual description of an AST statement."""
        return type(node).__name__ + (f"(line {node.line})" if node.line else "")

    # ── AST visitor (returns the id of the last block produced) ──────────────

    def _visit(self, node: Any, pred_id: int) -> Optional[int]:
        """Visit a node; wire its blocks after *pred_id*. Returns last block id."""
        if node is None:
            return pred_id
        if isinstance(node, list):
            cur = pred_id
            for item in node:
                cur = self._visit(item, cur) or cur
            return cur
        if not isinstance(node, ASTNode):
            return pred_id

        method = f"_visit_{type(node).__name__}"
        handler = getattr(self, method, self._visit_statement)
        return handler(node, pred_id)

    def _visit_Program(self, node: Program, pred_id: int) -> int:
        cur = pred_id
        for stmt in node.statements:
            cur = self._visit(stmt, cur) or cur
        return cur

    def _visit_FunctionDecl(self, node: FunctionDecl, pred_id: int) -> int:
        func_block = self._new_block(f"FUNC:{node.name}")
        self._add_edge(pred_id, func_block.block_id)
        func_block.stmts.append(f"FunctionDecl '{node.name}' (line {node.line})")
        func_block.stmt_lines.append(node.line)
        last = func_block.block_id
        if node.body:
            last = self._visit_Block(node.body, func_block.block_id)
        return last

    def _visit_ClassDecl(self, node: ClassDecl, pred_id: int) -> int:
        cur = pred_id
        for method in node.methods:
            cur = self._visit(method, cur) or cur
        return cur

    def _visit_Block(self, node: Block, pred_id: int) -> int:
        cur = pred_id
        for stmt in node.statements:
            cur = self._visit(stmt, cur) or cur
        return cur

    def _visit_IfStmt(self, node: IfStmt, pred_id: int) -> int:
        cond_block = self._new_block(f"IF(line {node.line})")
        self._add_edge(pred_id, cond_block.block_id)
        cond_block.stmts.append(f"if-condition (line {node.line})")
        cond_block.stmt_lines.append(node.line)

        # Then-branch
        then_end = cond_block.block_id
        if node.then_block:
            then_entry = self._new_block("THEN")
            self._add_edge(cond_block.block_id, then_entry.block_id, "true_branch")
            then_end = self._visit_Block(node.then_block, then_entry.block_id)

        # Else-branch
        else_end = cond_block.block_id
        if node.else_block:
            else_entry = self._new_block("ELSE")
            self._add_edge(cond_block.block_id, else_entry.block_id, "false_branch")
            else_end = self._visit_Block(node.else_block, else_entry.block_id)
        else:
            else_end = cond_block.block_id   # fall-through

        # Merge block
        merge = self._new_block("MERGE")
        self._add_edge(then_end, merge.block_id)
        self._add_edge(else_end, merge.block_id)
        return merge.block_id

    def _visit_WhileStmt(self, node: WhileStmt, pred_id: int) -> int:
        header = self._new_block(f"LOOP:while(line {node.line})")
        self._add_edge(pred_id, header.block_id)
        header.stmts.append(f"while-condition (line {node.line})")
        header.stmt_lines.append(node.line)

        body_end = header.block_id
        if node.body:
            body_entry = self._new_block("BODY")
            self._add_edge(header.block_id, body_entry.block_id, "true_branch")
            body_end = self._visit_Block(node.body, body_entry.block_id)

        # Back-edge
        self._add_edge(body_end, header.block_id, "loop_back")

        # Exit block (false-branch of condition)
        exit_blk = self._new_block("LOOP_EXIT")
        self._add_edge(header.block_id, exit_blk.block_id, "false_branch")
        return exit_blk.block_id

    def _visit_ForStmt(self, node: ForStmt, pred_id: int) -> int:
        header = self._new_block(f"LOOP:for(line {node.line})")
        self._add_edge(pred_id, header.block_id)
        header.stmts.append(f"for-loop (line {node.line})")
        header.stmt_lines.append(node.line)

        body_end = header.block_id
        if node.body:
            body_entry = self._new_block("BODY")
            self._add_edge(header.block_id, body_entry.block_id, "true_branch")
            body_end = self._visit_Block(node.body, body_entry.block_id)

        # Back-edge (via increment)
        incr_block = self._new_block("INCR")
        self._add_edge(body_end, incr_block.block_id)
        self._add_edge(incr_block.block_id, header.block_id, "loop_back")

        exit_blk = self._new_block("LOOP_EXIT")
        self._add_edge(header.block_id, exit_blk.block_id, "false_branch")
        return exit_blk.block_id

    def _visit_ReturnStmt(self, node: ReturnStmt, pred_id: int) -> int:
        blk = self._new_block(f"RETURN(line {node.line})")
        self._add_edge(pred_id, blk.block_id)
        blk.stmts.append(f"return (line {node.line})")
        blk.stmt_lines.append(node.line)
        return blk.block_id

    def _visit_statement(self, node: ASTNode, pred_id: int) -> int:
        """Generic handler for simple statements (variable decl, expr, etc.)."""
        # Find or extend a straight-line "stmt" block after pred_id
        # to keep sequential blocks minimal
        blk = self._new_block(f"STMT(line {node.line})")
        self._add_edge(pred_id, blk.block_id)
        blk.stmts.append(self._stmt_summary(node))
        blk.stmt_lines.append(node.line)
        return blk.block_id

    # ── CFG analysis helpers ──────────────────────────────────────────────────

    def _find_unreachable(self) -> List[int]:
        """DFS from the ENTRY block; blocks not visited are unreachable."""
        if not self._blocks:
            return []
        reachable: Set[int] = set()
        stack = [0]   # ENTRY always has id = 0
        adj: Dict[int, List[int]] = {}
        for e in self._edges:
            adj.setdefault(e.from_id, []).append(e.to_id)
        while stack:
            node_id = stack.pop()
            if node_id in reachable:
                continue
            reachable.add(node_id)
            stack.extend(adj.get(node_id, []))
        all_ids = {b.block_id for b in self._blocks}
        return sorted(all_ids - reachable)

    def _find_loops(self) -> List[Dict]:
        """Report back-edges as detected loops."""
        loops = []
        for e in self._edges:
            if e.edge_type == "loop_back":
                header = next((b for b in self._blocks if b.block_id == e.to_id), None)
                loops.append({
                    "header_block":    e.to_id,
                    "header_label":    header.label if header else "",
                    "back_edge_from":  e.from_id,
                })
        return loops
