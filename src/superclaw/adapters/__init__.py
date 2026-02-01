"""SuperClaw Agent Adapters.

Adapters connect SuperClaw to different AI coding agents.
"""

from superclaw.adapters.base import AgentAdapter, AgentOutput
from superclaw.adapters.mock import MockAdapter
from superclaw.adapters.openclaw import OpenClawAdapter

__all__ = [
    "AgentAdapter",
    "AgentOutput",
    "OpenClawAdapter",
    "MockAdapter",
    "ADAPTER_REGISTRY",
    "create_adapter",
]

ADAPTER_REGISTRY = {
    "openclaw": OpenClawAdapter,
    "mock": MockAdapter,
}


def create_adapter(agent_type: str, config: dict | None = None) -> AgentAdapter:
    """
    Factory function to create an adapter.

    Args:
        agent_type: Type of agent (openclaw, acp, etc.)
        config: Optional configuration

    Returns:
        AgentAdapter instance

    Raises:
        ValueError: If adapter not found
    """
    if agent_type not in ADAPTER_REGISTRY:
        available = ", ".join(ADAPTER_REGISTRY.keys())
        raise ValueError(f"Unknown agent type: {agent_type}. Available: {available}")

    adapter_class = ADAPTER_REGISTRY[agent_type]
    return adapter_class(config=config or {})
