"""
self_heal — Self-Healing Compiler Module
=========================================
Provides automatic error-repair capabilities for the ML-Powered Syntax
Error Analyzer.

Public API
----------
    from self_heal import heal_source, HealResult

    result = heal_source(source, errors, language="python")
    # result.healed_source  — repaired source text
    # result.actions        — list[RepairAction]
    # result.repaired_count — number of successfully verified repairs
    # result.fully_healed   — True if every error got a verified fix
"""

from self_heal.healer import heal_source, HealResult, RepairAction

__all__ = ["heal_source", "HealResult", "RepairAction"]
