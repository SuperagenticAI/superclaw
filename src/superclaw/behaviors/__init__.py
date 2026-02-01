"""SuperClaw Security Behaviors.

Behaviors define what security properties to test in AI agents.
"""

from superclaw.behaviors.base import (
    BehaviorContract,
    BehaviorResult,
    BehaviorSpec,
    Severity,
)
from superclaw.behaviors.injection_resistance import PromptInjectionResistance
from superclaw.behaviors.tool_policy import ToolPolicyEnforcement
from superclaw.behaviors.sandbox_isolation import SandboxIsolation
from superclaw.behaviors.session_boundary import SessionBoundaryIntegrity
from superclaw.behaviors.config_drift import ConfigurationDriftDetection
from superclaw.behaviors.protocol_security import ACPProtocolSecurity

__all__ = [
    "BehaviorContract",
    "BehaviorResult",
    "BehaviorSpec",
    "Severity",
    "PromptInjectionResistance",
    "ToolPolicyEnforcement",
    "SandboxIsolation",
    "SessionBoundaryIntegrity",
    "ConfigurationDriftDetection",
    "ACPProtocolSecurity",
    "BEHAVIOR_REGISTRY",
    "create_behavior",
]

BEHAVIOR_REGISTRY = {
    "prompt-injection-resistance": PromptInjectionResistance,
    "tool-policy-enforcement": ToolPolicyEnforcement,
    "sandbox-isolation": SandboxIsolation,
    "session-boundary-integrity": SessionBoundaryIntegrity,
    "configuration-drift-detection": ConfigurationDriftDetection,
    "acp-protocol-security": ACPProtocolSecurity,
}


def create_behavior(name: str, config: dict | None = None) -> BehaviorSpec:
    """
    Factory function to create a behavior.

    Args:
        name: Behavior name
        config: Optional configuration

    Returns:
        BehaviorSpec instance

    Raises:
        ValueError: If behavior not found
    """
    if name not in BEHAVIOR_REGISTRY:
        available = ", ".join(BEHAVIOR_REGISTRY.keys())
        raise ValueError(f"Unknown behavior: {name}. Available: {available}")

    behavior_class = BEHAVIOR_REGISTRY[name]
    return behavior_class(config=config or {})
