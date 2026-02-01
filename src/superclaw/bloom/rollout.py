"""RolloutEngine for executing scenarios against agent adapters."""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field
from typing import Any, Protocol


class AgentAdapter(Protocol):
    """Protocol for agent adapters that can process prompts."""

    async def process(self, prompt: str) -> str:
        """Process a prompt and return the agent's response."""
        ...


@dataclass
class RolloutResult:
    """Result from executing a single scenario."""

    scenario_id: str
    prompt: str
    output: str
    start_time: float
    end_time: float
    duration_ms: float
    success: bool
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "scenario_id": self.scenario_id,
            "prompt": self.prompt,
            "output": self.output,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration_ms": self.duration_ms,
            "success": self.success,
            "error": self.error,
            "metadata": self.metadata,
        }


class RolloutEngine:
    """Engine for executing scenarios against an agent adapter."""

    def __init__(
        self,
        adapter: AgentAdapter,
        concurrency: int = 5,
        timeout: float = 60.0,
    ) -> None:
        """Initialize the RolloutEngine.

        Args:
            adapter: The agent adapter to test.
            concurrency: Maximum number of concurrent scenario executions.
            timeout: Timeout in seconds for each scenario execution.
        """
        self.adapter = adapter
        self.concurrency = concurrency
        self.timeout = timeout

    def execute(
        self,
        scenarios: list[dict[str, Any]],
    ) -> list[RolloutResult]:
        """Execute scenarios synchronously.

        Args:
            scenarios: List of scenario dictionaries to execute.

        Returns:
            List of RolloutResult objects.
        """
        return asyncio.run(self.aexecute(scenarios))

    async def aexecute(
        self,
        scenarios: list[dict[str, Any]],
    ) -> list[RolloutResult]:
        """Execute scenarios asynchronously with concurrency control.

        Args:
            scenarios: List of scenario dictionaries to execute.

        Returns:
            List of RolloutResult objects.
        """
        semaphore = asyncio.Semaphore(self.concurrency)
        tasks = [
            self._execute_with_semaphore(semaphore, scenario)
            for scenario in scenarios
        ]
        results = await asyncio.gather(*tasks)
        return list(results)

    async def _execute_with_semaphore(
        self,
        semaphore: asyncio.Semaphore,
        scenario: dict[str, Any],
    ) -> RolloutResult:
        """Execute a single scenario with semaphore control."""
        async with semaphore:
            return await self._execute_scenario(scenario)

    async def _execute_scenario(
        self,
        scenario: dict[str, Any],
    ) -> RolloutResult:
        """Execute a single scenario against the adapter.

        Args:
            scenario: The scenario to execute.

        Returns:
            RolloutResult with execution details.
        """
        scenario_id = scenario.get("id", "unknown")
        prompt = scenario.get("prompt", "")
        start_time = time.time()

        try:
            output = await asyncio.wait_for(
                self.adapter.process(prompt),
                timeout=self.timeout,
            )
            end_time = time.time()
            duration_ms = (end_time - start_time) * 1000

            return RolloutResult(
                scenario_id=scenario_id,
                prompt=prompt,
                output=output,
                start_time=start_time,
                end_time=end_time,
                duration_ms=duration_ms,
                success=True,
                metadata={
                    "behavior": scenario.get("behavior"),
                    "difficulty": scenario.get("difficulty"),
                    "expected_behavior": scenario.get("expected_behavior"),
                },
            )

        except asyncio.TimeoutError:
            end_time = time.time()
            duration_ms = (end_time - start_time) * 1000
            return RolloutResult(
                scenario_id=scenario_id,
                prompt=prompt,
                output="",
                start_time=start_time,
                end_time=end_time,
                duration_ms=duration_ms,
                success=False,
                error=f"Timeout after {self.timeout}s",
                metadata={"behavior": scenario.get("behavior")},
            )

        except Exception as e:
            end_time = time.time()
            duration_ms = (end_time - start_time) * 1000
            return RolloutResult(
                scenario_id=scenario_id,
                prompt=prompt,
                output="",
                start_time=start_time,
                end_time=end_time,
                duration_ms=duration_ms,
                success=False,
                error=str(e),
                metadata={"behavior": scenario.get("behavior")},
            )

    async def execute_single(
        self,
        scenario: dict[str, Any],
    ) -> RolloutResult:
        """Execute a single scenario.

        Args:
            scenario: The scenario to execute.

        Returns:
            RolloutResult with execution details.
        """
        return await self._execute_scenario(scenario)
