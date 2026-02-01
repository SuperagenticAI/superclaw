"""SuperClaw - Agent Security Testing Framework.

Break AI coding agents with CodeOptiX and Bloom.
"""

__version__ = "0.1.0"
__author__ = "Superagentic AI"

from superclaw.attacks import ATTACK_REGISTRY
from superclaw.behaviors import BEHAVIOR_REGISTRY

__all__ = [
    "__version__",
    "BEHAVIOR_REGISTRY",
    "ATTACK_REGISTRY",
]
