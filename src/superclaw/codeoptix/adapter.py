"""Adapter to bridge SuperClaw behaviors to CodeOptiX BehaviorSpec.

This allows SuperClaw security behaviors to be used within CodeOptiX's
evaluation engine and benefit from its multi-modal evaluation pipeline.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from codeoptix.behaviors.base import BehaviorResult as CodeOptixBehaviorResult

from superclaw.adapters.base import AgentOutput
from superclaw.behaviors import BEHAVIOR_REGISTRY, BehaviorResult, BehaviorSpec, Severity


def _codeoptix_available() -> bool:
    """Check if CodeOptiX is installed."""
    from importlib.util import find_spec

    return find_spec("codeoptix") is not None


class SuperClawBehaviorAdapter:
    """
    Adapts a SuperClaw security behavior to work with CodeOptiX.

    This adapter wraps a SuperClaw BehaviorSpec and exposes it as a
    CodeOptiX-compatible BehaviorSpec, enabling:
    - Use within CodeOptiX's EvaluationEngine
    - Multi-modal evaluation (static analysis + LLM + tests)
    - Bloom-style scenario generation
    """

    def __init__(self, superclaw_behavior: BehaviorSpec):
        """
        Initialize adapter with a SuperClaw behavior.

        Args:
            superclaw_behavior: SuperClaw BehaviorSpec to adapt
        """
        self.superclaw_behavior = superclaw_behavior
        self.name = superclaw_behavior.name
        self.severity = superclaw_behavior.severity
        self.enabled = superclaw_behavior.enabled
        self.config = superclaw_behavior.config

    def get_name(self) -> str:
        """Get behavior name."""
        return self.superclaw_behavior.name

    def get_description(self) -> str:
        """Get behavior description."""
        return self.superclaw_behavior.get_description()

    def is_enabled(self) -> bool:
        """Check if behavior is enabled."""
        return self.superclaw_behavior.is_enabled()

    def get_severity(self) -> Severity:
        """Get severity level."""
        return self.superclaw_behavior.get_severity()

    def evaluate(
        self,
        agent_output: Any,
        context: dict[str, Any] | None = None,
    ) -> BehaviorResult:
        """
        Evaluate agent output using SuperClaw behavior.

        Converts CodeOptiX AgentOutput to SuperClaw AgentOutput format
        if necessary.

        Args:
            agent_output: Output from agent (CodeOptiX or SuperClaw format)
            context: Evaluation context

        Returns:
            BehaviorResult from evaluation
        """
        # Convert CodeOptiX AgentOutput to SuperClaw AgentOutput if needed
        if hasattr(agent_output, "code") and not hasattr(agent_output, "tool_calls"):
            # This is a CodeOptiX AgentOutput, convert it
            superclaw_output = self._convert_to_superclaw_output(agent_output)
        else:
            superclaw_output = agent_output

        return self.superclaw_behavior.evaluate(superclaw_output, context)

    def _convert_to_superclaw_output(self, codeoptix_output: Any) -> AgentOutput:
        """
        Convert CodeOptiX AgentOutput to SuperClaw AgentOutput.

        Args:
            codeoptix_output: CodeOptiX AgentOutput

        Returns:
            SuperClaw AgentOutput
        """
        return AgentOutput(
            code=getattr(codeoptix_output, "code", "") or "",
            tests=getattr(codeoptix_output, "tests", "") or "",
            response_text=getattr(codeoptix_output, "code", "") or "",
            tool_calls=[],
            tool_results=[],
            session_metadata=getattr(codeoptix_output, "metadata", {}) or {},
            acp_messages=[],
            sandbox_access_log=[],
            injection_attempts_detected=[],
        )


def adapt_behavior_to_codeoptix(behavior_name: str, config: dict[str, Any] | None = None):
    """
    Create a CodeOptiX-compatible behavior from a SuperClaw behavior.

    Args:
        behavior_name: Name of SuperClaw behavior
        config: Optional configuration

    Returns:
        Adapted behavior that works with CodeOptiX

    Raises:
        ValueError: If behavior not found
    """
    from superclaw.behaviors import create_behavior

    superclaw_behavior = create_behavior(behavior_name, config)
    return SuperClawBehaviorAdapter(superclaw_behavior)


def register_superclaw_behaviors() -> dict[str, type]:
    """
    Register all SuperClaw security behaviors with CodeOptiX.

    This extends CodeOptiX's BEHAVIOR_REGISTRY with SuperClaw's
    security behaviors, allowing them to be used via CodeOptiX's
    create_behavior() factory.

    Returns:
        Dictionary of registered behavior names to adapter factories

    Raises:
        RuntimeError: If CodeOptiX is not installed
    """
    if not _codeoptix_available():
        raise RuntimeError("CodeOptiX not installed. Install with: pip install codeoptix")

    from codeoptix.behaviors import BEHAVIOR_REGISTRY as CODEOPTIX_REGISTRY

    registered = {}

    for name, behavior_class in BEHAVIOR_REGISTRY.items():
        # Prefix with 'security-' to avoid conflicts
        codeoptix_name = f"security-{name}" if not name.startswith("security-") else name

        # Create a factory that returns adapted behavior
        def make_factory(behavior_cls):
            def factory(config=None):
                superclaw_behavior = behavior_cls(config)
                return SuperClawBehaviorAdapter(superclaw_behavior)

            return factory

        CODEOPTIX_REGISTRY[codeoptix_name] = make_factory(behavior_class)
        registered[codeoptix_name] = behavior_class

    return registered


def get_codeoptix_behavior_result(
    superclaw_result: BehaviorResult,
) -> CodeOptixBehaviorResult:
    """
    Convert SuperClaw BehaviorResult to CodeOptiX BehaviorResult.

    Args:
        superclaw_result: SuperClaw behavior result

    Returns:
        CodeOptiX-compatible BehaviorResult
    """
    if not _codeoptix_available():
        raise RuntimeError("CodeOptiX not installed")

    from codeoptix.behaviors.base import BehaviorResult as COBehaviorResult
    from codeoptix.behaviors.base import Severity as COSeverity

    # Map severity
    severity_map = {
        Severity.LOW: COSeverity.LOW,
        Severity.MEDIUM: COSeverity.MEDIUM,
        Severity.HIGH: COSeverity.HIGH,
        Severity.CRITICAL: COSeverity.CRITICAL,
    }

    return COBehaviorResult(
        behavior_name=superclaw_result.behavior_name,
        passed=superclaw_result.passed,
        score=superclaw_result.score,
        evidence=superclaw_result.evidence,
        severity=severity_map.get(superclaw_result.severity, COSeverity.MEDIUM),
        metadata=superclaw_result.metadata,
    )
