"""Base adapter for SuperClaw."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentOutput:
    """
    Output from an AI agent interaction.
    
    This captures all relevant data from an agent session for security evaluation.
    """

    # Standard output fields
    code: str = ""
    tests: str = ""
    response_text: str = ""

    # Tool interaction tracking
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    tool_results: list[dict[str, Any]] = field(default_factory=list)

    # Session and protocol data
    session_metadata: dict[str, Any] = field(default_factory=dict)
    acp_messages: list[dict[str, Any]] = field(default_factory=list)

    # Evidence ledger fields
    messages: list[dict[str, Any]] = field(default_factory=list)
    artifacts: list[dict[str, Any]] = field(default_factory=list)
    secrets_detected: list[dict[str, Any]] = field(default_factory=list)

    # Security-specific tracking
    sandbox_access_log: list[str] = field(default_factory=list)
    injection_attempts_detected: list[dict[str, Any]] = field(default_factory=list)

    # Timing and performance
    duration_ms: float = 0.0
    token_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "code": self.code,
            "tests": self.tests,
            "response_text": self.response_text,
            "tool_calls": self.tool_calls,
            "tool_results": self.tool_results,
            "session_metadata": self.session_metadata,
            "acp_messages": self.acp_messages,
            "messages": self.messages,
            "artifacts": self.artifacts,
            "secrets_detected": self.secrets_detected,
            "sandbox_access_log": self.sandbox_access_log,
            "injection_attempts_detected": self.injection_attempts_detected,
            "duration_ms": self.duration_ms,
            "token_count": self.token_count,
        }

    def to_ledger(self) -> dict[str, Any]:
        """Return a normalized evidence ledger."""
        return {
            "messages": self.messages,
            "tool_calls": self.tool_calls,
            "tool_results": self.tool_results,
            "artifacts": self.artifacts,
            "secrets_detected": self.secrets_detected,
        }


class AgentAdapter(ABC):
    """Base class for agent adapters."""

    def __init__(self, config: dict[str, Any] | None = None):
        """
        Initialize adapter.

        Args:
            config: Adapter-specific configuration
        """
        self.config = config or {}

    @abstractmethod
    async def connect(self) -> bool:
        """
        Connect to the agent.

        Returns:
            True if connection successful
        """

    @abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from the agent."""

    @abstractmethod
    async def send_prompt(
        self,
        prompt: str,
        context: dict[str, Any] | None = None,
    ) -> AgentOutput:
        """
        Send a prompt to the agent and get response.

        Args:
            prompt: The prompt/attack payload to send
            context: Optional context for the interaction

        Returns:
            AgentOutput with all captured data
        """

    @abstractmethod
    async def get_session_info(self) -> dict[str, Any]:
        """
        Get current session information.

        Returns:
            Session metadata dictionary
        """

    @abstractmethod
    def get_name(self) -> str:
        """Get adapter name."""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(config={self.config!r})"
