"""Mock adapter for offline SuperClaw testing."""

from __future__ import annotations

import itertools
import time
from typing import Any

from superclaw.adapters.base import AgentAdapter, AgentOutput


class MockAdapter(AgentAdapter):
    """Mock adapter that returns canned responses for offline testing."""

    def __init__(self, config: dict[str, Any] | None = None):
        super().__init__(config)
        responses = (self.config.get("responses") or ["Mock response"])
        self._responses = itertools.cycle(responses)
        self._connected = False

    def get_name(self) -> str:
        return "mock"

    async def connect(self) -> bool:
        self._connected = True
        return True

    async def disconnect(self) -> None:
        self._connected = False

    async def send_prompt(
        self,
        prompt: str,
        context: dict[str, Any] | None = None,
    ) -> AgentOutput:
        context = context or {}
        start = time.time()

        response_text = self._build_response(prompt, context)
        duration_ms = (time.time() - start) * 1000

        injection_attempts = []
        if self.config.get("simulate_injection", False):
            injection_attempts.append({"pattern": "mock", "blocked": False})

        tool_calls = self.config.get("tool_calls", [])
        tool_results = self.config.get("tool_results", [])

        return AgentOutput(
            response_text=response_text,
            tool_calls=list(tool_calls),
            tool_results=list(tool_results),
            messages=[
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": response_text},
            ],
            session_metadata={"mock": True},
            injection_attempts_detected=injection_attempts,
            duration_ms=duration_ms,
        )

    async def get_session_info(self) -> dict[str, Any]:
        return {"mock": True, "connected": self._connected}

    def _build_response(self, prompt: str, context: dict[str, Any]) -> str:
        if self.config.get("echo_prompt", False):
            return f"{next(self._responses)}\n\n[echo]\n{prompt}"
        return next(self._responses)
