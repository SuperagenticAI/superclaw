"""Base behavior specification for SuperClaw."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from superclaw.adapters.base import AgentOutput


class Severity(str, Enum):
    """Severity levels for security findings."""
    
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class BehaviorResult:
    """Result of behavior evaluation."""

    behavior_name: str
    passed: bool
    score: float  # 0.0 to 1.0 (1.0 = secure, 0.0 = vulnerable)
    evidence: list[str] = field(default_factory=list)
    severity: Severity = Severity.MEDIUM
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate score range."""
        if not 0.0 <= self.score <= 1.0:
            raise ValueError(f"Score must be between 0.0 and 1.0, got {self.score}")

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "behavior_name": self.behavior_name,
            "passed": self.passed,
            "score": self.score,
            "evidence": self.evidence,
            "severity": self.severity.value,
            "metadata": self.metadata,
        }


@dataclass(frozen=True)
class BehaviorContract:
    """Structured definition of a security behavior."""

    id: str
    intent: str
    setup_assumptions: list[str]
    attack_payloads: list[str]
    success_criteria: list[str]
    severity_rubric: list[str]
    evidence_extractors: list[str]
    mitigation: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "intent": self.intent,
            "setup_assumptions": self.setup_assumptions,
            "attack_payloads": self.attack_payloads,
            "success_criteria": self.success_criteria,
            "severity_rubric": self.severity_rubric,
            "evidence_extractors": self.evidence_extractors,
            "mitigation": self.mitigation,
        }


class BehaviorSpec(ABC):
    """Base class for security behavior specifications."""

    default_severity: Severity = Severity.MEDIUM

    def __init__(self, config: dict[str, Any] | None = None):
        """
        Initialize behavior spec.

        Args:
            config: Behavior-specific configuration
        """
        self.config = config or {}
        self.name = self.get_name()
        self.severity = Severity(self.config.get("severity", self.default_severity.value))
        self.enabled = self.config.get("enabled", True)
        self._contract = self.get_contract()
        self._validate_contract(self._contract)

    @abstractmethod
    def get_name(self) -> str:
        """Get the unique name identifier for this behavior."""

    @abstractmethod
    def get_description(self) -> str:
        """Get human-readable description of behavior."""

    @abstractmethod
    def get_contract(self) -> BehaviorContract:
        """Return the structured behavior contract."""

    @abstractmethod
    def evaluate(
        self,
        agent_output: "AgentOutput",
        context: dict[str, Any] | None = None,
    ) -> BehaviorResult:
        """
        Evaluate agent output against this behavior.

        Args:
            agent_output: Output from agent adapter
            context: Optional evaluation context

        Returns:
            BehaviorResult with evaluation results
        """

    def is_enabled(self) -> bool:
        """Check if this behavior is enabled."""
        return self.enabled

    def get_severity(self) -> Severity:
        """Get the severity level for this behavior."""
        return self.severity

    def get_contract_dict(self) -> dict[str, Any]:
        """Return behavior contract as a dictionary."""
        return self._contract.to_dict()

    def _validate_contract(self, contract: BehaviorContract) -> None:
        if not contract.id or not contract.intent:
            raise ValueError("Behavior contract requires non-empty id and intent")
        if not contract.attack_payloads:
            raise ValueError("Behavior contract requires attack_payloads")
        if not contract.success_criteria:
            raise ValueError("Behavior contract requires success_criteria")
        if not contract.severity_rubric:
            raise ValueError("Behavior contract requires severity_rubric")
        if not contract.mitigation:
            raise ValueError("Behavior contract requires mitigation")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, enabled={self.enabled})"
