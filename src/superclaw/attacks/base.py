"""Base attack class for SuperClaw."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class AttackResult:
    """Result of an attack attempt."""

    attack_name: str
    payload: str
    success: bool
    response: str = ""
    evidence: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "attack_name": self.attack_name,
            "payload": self.payload[:200],  # Truncate for safety
            "success": self.success,
            "response": self.response[:500],  # Truncate
            "evidence": self.evidence,
            "metadata": self.metadata,
        }


class Attack(ABC):
    """Base class for attack implementations."""

    attack_type: str = "unknown"
    description: str = ""

    def __init__(self, config: dict[str, Any] | None = None):
        """
        Initialize attack.

        Args:
            config: Attack-specific configuration
        """
        self.config = config or {}

    @abstractmethod
    def generate_payloads(self) -> list[str]:
        """
        Generate attack payloads.

        Returns:
            List of attack payload strings
        """

    @abstractmethod
    def evaluate_response(
        self,
        payload: str,
        response: str,
        context: dict[str, Any] | None = None,
    ) -> AttackResult:
        """
        Evaluate if attack was successful.

        Args:
            payload: The attack payload sent
            response: The agent's response
            context: Optional evaluation context

        Returns:
            AttackResult with success determination
        """

    def get_name(self) -> str:
        """Get attack name."""
        return self.__class__.__name__

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(type={self.attack_type!r})"
