"""OpenClaw adapter for SuperClaw."""

from __future__ import annotations

import asyncio
import json
import time
from typing import Any

from superclaw.adapters.base import AgentAdapter, AgentOutput


class OpenClawAdapter(AgentAdapter):
    """
    Adapter for OpenClaw agents via ACP protocol.

    Connects to OpenClaw gateway via WebSocket and manages
    ACP session communication.
    """

    def __init__(self, config: dict[str, Any] | None = None):
        super().__init__(config)
        self.target = (
            config.get("target", "ws://127.0.0.1:18789") if config else "ws://127.0.0.1:18789"
        )
        self.token = config.get("token") if config else None
        self.password = config.get("password") if config else None
        self.request_timeout = float(config.get("request_timeout", 120.0)) if config else 120.0
        self.open_timeout = float(config.get("open_timeout", 10.0)) if config else 10.0

        self._ws = None
        self._session_id = ""
        self._request_id = 0
        self._pending: dict[int, asyncio.Future] = {}
        self._acp_messages: list[dict] = []
        self._tool_calls: list[dict] = []
        self._tool_results: list[dict] = []
        self._read_task = None

    def get_name(self) -> str:
        return "openclaw"

    async def connect(self) -> bool:
        """Connect to OpenClaw gateway."""
        try:
            import websockets

            if not (self.target.startswith("ws://") or self.target.startswith("wss://")):
                raise ValueError("OpenClaw target must be a ws:// or wss:// URL")

            headers = {}
            if self.token:
                headers["Authorization"] = f"Bearer {self.token}"

            self._ws = await websockets.connect(
                self.target,
                additional_headers=headers if headers else None,
                open_timeout=self.open_timeout,
            )

            # Start reading messages
            self._read_task = asyncio.create_task(self._read_loop())

            # Initialize ACP
            await self._initialize()

            # Create session
            await self._create_session()

            if not self._session_id:
                raise RuntimeError("Failed to create ACP session")

            return True

        except Exception as e:
            print(f"Connection failed: {e}")
            return False

    async def disconnect(self) -> None:
        """Disconnect from OpenClaw gateway."""
        if self._read_task:
            self._read_task.cancel()
            try:
                await self._read_task
            except asyncio.CancelledError:
                pass

        if self._ws:
            await self._ws.close()
            self._ws = None

    async def send_prompt(
        self,
        prompt: str,
        context: dict[str, Any] | None = None,
    ) -> AgentOutput:
        """Send prompt to OpenClaw and capture response."""
        if not self._ws:
            raise ConnectionError("Not connected to OpenClaw gateway")
        if not self._session_id:
            raise RuntimeError("ACP session not initialized")

        context = context or {}
        start_time = time.time()

        # Clear tracking for new interaction
        self._acp_messages.clear()
        self._tool_calls.clear()
        self._tool_results.clear()

        # Prepare content blocks
        content_blocks = [{"type": "text", "text": prompt}]

        # Send prompt
        response = await self._call_method(
            "session/prompt",
            prompt=content_blocks,
            sessionId=self._session_id,
        )

        if response and isinstance(response, dict) and response.get("error"):
            raise RuntimeError(f"OpenClaw error: {response['error']}")

        duration_ms = (time.time() - start_time) * 1000

        # Extract response text
        response_text = ""
        if response:
            # Handle different response formats
            if isinstance(response, dict):
                response_text = response.get("text", "")
                if not response_text:
                    content = response.get("content", [])
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            response_text += block.get("text", "")

        # Build output
        return AgentOutput(
            response_text=response_text,
            tool_calls=self._tool_calls.copy(),
            tool_results=self._tool_results.copy(),
            acp_messages=self._acp_messages.copy(),
            messages=[
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": response_text},
            ],
            session_metadata=await self.get_session_info(),
            duration_ms=duration_ms,
        )

    async def get_session_info(self) -> dict[str, Any]:
        """Get current session information."""
        try:
            response = await self._call_method(
                "session/status",
                sessionId=self._session_id,
            )
            if response and isinstance(response, dict) and response.get("error"):
                return {"session_id": self._session_id, "error": response["error"]}
            return response or {}
        except Exception:
            return {"session_id": self._session_id}

    async def _initialize(self) -> None:
        """Initialize ACP protocol."""
        response = await self._call_method(
            "initialize",
            protocolVersion=1,
            clientInfo={
                "name": "superclaw",
                "version": "0.1.0",
            },
        )
        if response and isinstance(response, dict) and response.get("error"):
            raise RuntimeError(f"ACP initialize failed: {response['error']}")

    async def _create_session(self) -> None:
        """Create a new ACP session."""
        response = await self._call_method("session/new")
        if response and isinstance(response, dict) and response.get("error"):
            raise RuntimeError(f"ACP session/new failed: {response['error']}")
        if response:
            self._session_id = response.get("sessionId", "")

    async def _call_method(self, method: str, **params) -> dict[str, Any] | None:
        """Call an ACP method."""
        if not self._ws:
            raise ConnectionError("WebSocket is not connected")

        self._request_id += 1
        request_id = self._request_id

        message = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
            "params": params,
        }

        # Track message
        self._acp_messages.append(
            {
                "type": "request",
                "method": method,
                "params": params,
            }
        )

        # Create future for response
        future: asyncio.Future = asyncio.Future()
        self._pending[request_id] = future

        # Send message
        await self._ws.send(json.dumps(message))

        # Wait for response
        try:
            response = await asyncio.wait_for(future, timeout=self.request_timeout)
            return response
        except TimeoutError:
            del self._pending[request_id]
            return None

    async def _read_loop(self) -> None:
        """Read messages from WebSocket."""
        try:
            async for message in self._ws:
                await self._handle_message(message)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"Read loop error: {e}")

    async def _handle_message(self, raw: str) -> None:
        """Handle incoming message."""
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return

        # Track all messages
        self._acp_messages.append(
            {
                "type": "response" if "id" in data else "notification",
                **data,
            }
        )

        # Handle response
        if "id" in data:
            request_id = data["id"]
            if request_id in self._pending:
                future = self._pending.pop(request_id)
                if "error" in data:
                    future.set_result({"error": data["error"]})
                else:
                    future.set_result(data.get("result", {}))

        # Handle notifications
        method = data.get("method", "")
        params = data.get("params", {})

        if method == "tool/call":
            self._tool_calls.append(params)
        elif method == "tool/result":
            self._tool_results.append(params)
