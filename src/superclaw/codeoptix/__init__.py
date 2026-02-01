"""CodeOptiX integration for SuperClaw.

This module provides hooks to use SuperClaw security behaviors
with CodeOptiX's evaluation engine and multi-modal evaluation.
"""

from superclaw.codeoptix.adapter import (
    SuperClawBehaviorAdapter,
    adapt_behavior_to_codeoptix,
    register_superclaw_behaviors,
)
from superclaw.codeoptix.engine import (
    SecurityEvaluationEngine,
    create_security_engine,
)
from superclaw.codeoptix.evaluator import (
    SecurityEvaluator,
    create_security_evaluator,
)

__all__ = [
    "SuperClawBehaviorAdapter",
    "adapt_behavior_to_codeoptix",
    "register_superclaw_behaviors",
    "SecurityEvaluator",
    "create_security_evaluator",
    "SecurityEvaluationEngine",
    "create_security_engine",
]
