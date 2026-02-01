"""Security evaluation engine that extends CodeOptiX's EvaluationEngine.

This provides a complete security testing workflow with:
- Scenario generation (via Bloom)
- Multi-modal evaluation
- Behavior-based scoring
- Result aggregation
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from superclaw.adapters.base import AgentAdapter, AgentOutput
from superclaw.behaviors import BEHAVIOR_REGISTRY, create_behavior
from superclaw.codeoptix.evaluator import SecurityEvaluationResult, SecurityEvaluator


@dataclass
class SecurityEngineResult:
    """Result from security evaluation engine."""

    agent_type: str
    target: str
    timestamp: str
    overall_score: float
    overall_passed: bool

    behaviors: dict[str, SecurityEvaluationResult] = field(default_factory=dict)
    scenarios_tested: int = 0
    scenarios_passed: int = 0

    summary: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "agent_type": self.agent_type,
            "target": self.target,
            "timestamp": self.timestamp,
            "overall_score": self.overall_score,
            "overall_passed": self.overall_passed,
            "behaviors": {name: result.to_dict() for name, result in self.behaviors.items()},
            "scenarios_tested": self.scenarios_tested,
            "scenarios_passed": self.scenarios_passed,
            "summary": self.summary,
            "metadata": self.metadata,
        }


class SecurityEvaluationEngine:
    """
    Security evaluation engine that mirrors CodeOptiX's EvaluationEngine.

    Provides a complete security testing workflow:
    1. Generate scenarios (via Bloom or templates)
    2. Execute scenarios against agent
    3. Evaluate responses for security issues
    4. Aggregate and report results
    """

    def __init__(
        self,
        adapter: AgentAdapter,
        llm_client: Any | None = None,
        config: dict[str, Any] | None = None,
    ):
        """
        Initialize security evaluation engine.

        Args:
            adapter: Agent adapter for executing prompts
            llm_client: Optional LLM client for LLM-as-judge evaluation
            config: Configuration dictionary
        """
        self.adapter = adapter
        self.llm_client = llm_client
        self.config = config or {}

        # Initialize security evaluator
        self.evaluator = SecurityEvaluator(
            llm_client=llm_client,
            config=self.config.get("evaluator", {}),
        )

        # Initialize scenario generator
        self._scenario_generator = None

    def evaluate_security(
        self,
        behavior_names: list[str] | None = None,
        scenarios: list[dict[str, Any]] | None = None,
        context: dict[str, Any] | None = None,
    ) -> SecurityEngineResult:
        """
        Evaluate agent security across behaviors.

        Args:
            behavior_names: Behaviors to evaluate (None = all)
            scenarios: Optional pre-generated scenarios
            context: Evaluation context

        Returns:
            SecurityEngineResult with full evaluation
        """
        context = context or {}
        behavior_names = behavior_names or list(BEHAVIOR_REGISTRY.keys())

        # Generate scenarios if not provided
        if not scenarios:
            scenarios = self._generate_scenarios(behavior_names)

        # Track results
        all_behavior_results: dict[str, SecurityEvaluationResult] = {}
        scenarios_tested = 0
        scenarios_passed = 0

        # Evaluate each behavior
        for behavior_name in behavior_names:
            if behavior_name not in BEHAVIOR_REGISTRY:
                continue

            # Get scenarios for this behavior
            behavior_scenarios = [s for s in scenarios if s.get("behavior") == behavior_name]

            if not behavior_scenarios:
                # Generate a default scenario
                behavior = create_behavior(behavior_name)
                behavior_scenarios = [
                    {
                        "behavior": behavior_name,
                        "prompt": f"Test scenario for {behavior.get_description()}",
                        "task": f"Security test: {behavior_name}",
                    }
                ]

            # Evaluate behavior across scenarios
            behavior_result = self._evaluate_behavior(
                behavior_name=behavior_name,
                scenarios=behavior_scenarios,
                context=context,
            )

            all_behavior_results[behavior_name] = behavior_result
            scenarios_tested += len(behavior_scenarios)
            if behavior_result.passed:
                scenarios_passed += len(behavior_scenarios)

        # Calculate overall results
        if all_behavior_results:
            scores = [r.score for r in all_behavior_results.values()]
            overall_score = sum(scores) / len(scores)
            overall_passed = all(r.passed for r in all_behavior_results.values())
        else:
            overall_score = 0.0
            overall_passed = True

        # Generate summary
        summary = self._generate_summary(all_behavior_results)

        return SecurityEngineResult(
            agent_type=self.adapter.get_name() if hasattr(self.adapter, "get_name") else "unknown",
            target=self.adapter.config.get("target", "unknown"),
            timestamp=datetime.now().isoformat(),
            overall_score=overall_score,
            overall_passed=overall_passed,
            behaviors=all_behavior_results,
            scenarios_tested=scenarios_tested,
            scenarios_passed=scenarios_passed,
            summary=summary,
            metadata={
                "config": self.config,
                "behaviors_tested": len(all_behavior_results),
            },
        )

    def _evaluate_behavior(
        self,
        behavior_name: str,
        scenarios: list[dict[str, Any]],
        context: dict[str, Any],
    ) -> SecurityEvaluationResult:
        """
        Evaluate a single behavior across scenarios.

        Args:
            behavior_name: Behavior to evaluate
            scenarios: Scenarios to test
            context: Evaluation context

        Returns:
            Aggregated SecurityEvaluationResult
        """
        all_evidence = []
        all_patterns = []
        scores = []
        passed_count = 0
        static_results = []
        llm_results = []

        for scenario in scenarios:
            # Execute agent with scenario prompt
            prompt = scenario.get("prompt", "")

            try:
                import asyncio

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                async def run():
                    connected = await self.adapter.connect()
                    if not connected:
                        return None
                    try:
                        return await self.adapter.send_prompt(prompt, context)
                    finally:
                        await self.adapter.disconnect()

                agent_output = loop.run_until_complete(run())
                loop.close()

                if agent_output is None:
                    continue

            except Exception:
                # Create empty output for failed execution
                agent_output = AgentOutput()

            # Evaluate using security evaluator
            eval_results = self.evaluator.evaluate(
                agent_output=agent_output,
                behavior_names=[behavior_name],
                context=context,
            )

            if behavior_name in eval_results:
                result = eval_results[behavior_name]
                all_evidence.extend(result.evidence)
                all_patterns.extend(result.pattern_matches)
                scores.append(result.score)
                if result.passed:
                    passed_count += 1
                if result.static_analysis:
                    static_results.append(result.static_analysis)
                if result.llm_evaluation:
                    llm_results.append(result.llm_evaluation)

        # Aggregate results
        avg_score = sum(scores) / len(scores) if scores else 0.0
        passed = passed_count == len(scenarios) if scenarios else True

        behavior = create_behavior(behavior_name)

        return SecurityEvaluationResult(
            behavior_name=behavior_name,
            passed=passed,
            score=avg_score,
            evidence=all_evidence[:20],  # Limit evidence
            severity=behavior.severity.value,
            static_analysis=static_results[0] if static_results else {},
            llm_evaluation=llm_results[0] if llm_results else {},
            pattern_matches=all_patterns[:10],  # Limit patterns
            metadata={
                "scenarios_tested": len(scenarios),
                "scenarios_passed": passed_count,
                "min_score": min(scores) if scores else 0.0,
                "max_score": max(scores) if scores else 0.0,
            },
        )

    def _generate_scenarios(
        self,
        behavior_names: list[str],
    ) -> list[dict[str, Any]]:
        """Generate scenarios for behaviors."""
        try:
            from superclaw.bloom import generate_scenarios

            all_scenarios = []
            for behavior_name in behavior_names:
                scenarios = generate_scenarios(
                    behavior=behavior_name,
                    num_scenarios=self.config.get("scenarios_per_behavior", 3),
                )
                for s in scenarios:
                    s["behavior"] = behavior_name
                all_scenarios.extend(scenarios)

            return all_scenarios

        except Exception:
            # Fallback to basic scenarios
            return self._generate_basic_scenarios(behavior_names)

    def _generate_basic_scenarios(
        self,
        behavior_names: list[str],
    ) -> list[dict[str, Any]]:
        """Generate basic test scenarios."""
        scenarios = []

        for behavior_name in behavior_names:
            behavior = create_behavior(behavior_name)

            scenarios.append(
                {
                    "behavior": behavior_name,
                    "prompt": f"Test: {behavior.get_description()}",
                    "task": f"Security test for {behavior_name}",
                }
            )

        return scenarios

    def _generate_summary(
        self,
        results: dict[str, SecurityEvaluationResult],
    ) -> dict[str, Any]:
        """Generate summary statistics."""
        if not results:
            return {}

        passed = sum(1 for r in results.values() if r.passed)
        failed = len(results) - passed

        # Count by severity
        severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for result in results.values():
            if not result.passed:
                severity = result.severity.lower()
                if severity in severity_counts:
                    severity_counts[severity] += 1

        return {
            "total_behaviors": len(results),
            "passed": passed,
            "failed": failed,
            "critical": severity_counts["critical"],
            "high": severity_counts["high"],
            "medium": severity_counts["medium"],
            "low": severity_counts["low"],
        }


def create_security_engine(
    adapter: AgentAdapter,
    llm_provider: str | None = None,
    config: dict[str, Any] | None = None,
) -> SecurityEvaluationEngine:
    """
    Factory function to create a security evaluation engine.

    Args:
        adapter: Agent adapter for executing prompts
        llm_provider: Optional LLM provider for evaluation
        config: Configuration dictionary

    Returns:
        Configured SecurityEvaluationEngine
    """
    llm_client = None

    if llm_provider:
        try:
            from codeoptix.utils.llm import LLMProvider, create_llm_client

            provider_map = {
                "openai": LLMProvider.OPENAI,
                "anthropic": LLMProvider.ANTHROPIC,
                "google": LLMProvider.GOOGLE,
                "ollama": LLMProvider.OLLAMA,
            }

            if llm_provider.lower() in provider_map:
                llm_client = create_llm_client(provider_map[llm_provider.lower()])
        except ImportError:
            pass

    return SecurityEvaluationEngine(
        adapter=adapter,
        llm_client=llm_client,
        config=config,
    )
