# Adapters API

Python API reference for agent communication adapters.

---

## AgentAdapter Base Class

All adapters inherit from the `AgentAdapter` abstract base class.

```python
from superclaw.adapters.base import AgentAdapter, AgentOutput

class AgentAdapter(ABC):
    """Base class for agent communication adapters."""
    
    @abstractmethod
    async def connect(self) -> bool:
        """Establish connection to the target agent.
        
        Returns:
            True if connection successful, False otherwise.
        """
        ...

    @abstractmethod
    async def disconnect(self) -> None:
        """Cleanly close the connection."""
        ...

    @abstractmethod
    async def send_prompt(
        self, 
        prompt: str, 
        context: dict | None = None
    ) -> AgentOutput:
        """Send a prompt and return the agent's response.
        
        Args:
            prompt: The message to send to the agent.
            context: Optional context (session ID, metadata, etc.)
            
        Returns:
            AgentOutput containing response and evidence.
        """
        ...
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the agent is healthy and responsive.
        
        Returns:
            True if agent is healthy, False otherwise.
        """
        ...
```

---

## AgentOutput

Structured output from an agent interaction.

```python
from superclaw.adapters.base import AgentOutput

@dataclass
class AgentOutput:
    response_text: str | None
    """The agent's text response."""
    
    tool_calls: list[ToolCall]
    """Tools the agent attempted to call."""
    
    tool_results: list[ToolResult]
    """Results from tool executions."""
    
    artifacts: list[Artifact]
    """Files, URLs, or other artifacts touched."""
    
    secrets_detected: list[str]
    """Any detected secrets or sensitive patterns."""
    
    raw_response: dict | None = None
    """Raw response from the agent for debugging."""
    
    metadata: dict = field(default_factory=dict)
    """Additional metadata."""
```

---

## Supporting Types

### ToolCall

```python
@dataclass
class ToolCall:
    name: str
    """Name of the tool called."""
    
    args: dict
    """Arguments passed to the tool."""
    
    timestamp: datetime | None = None
    """When the call was made."""
```

### ToolResult

```python
@dataclass
class ToolResult:
    name: str
    """Name of the tool."""
    
    output: str
    """Tool output/result."""
    
    success: bool
    """Whether the tool execution succeeded."""
    
    error: str | None = None
    """Error message if failed."""
```

### Artifact

```python
@dataclass
class Artifact:
    type: str
    """Type of artifact: 'file', 'url', 'database', etc."""
    
    path: str
    """Path or identifier."""
    
    action: str
    """Action taken: 'read', 'write', 'delete', etc."""
    
    metadata: dict = field(default_factory=dict)
    """Additional artifact metadata."""
```

---

## Built-in Adapters

### OpenClawAdapter

Communicates with OpenClaw agents via ACP WebSocket.

```python
from superclaw.adapters import OpenClawAdapter

adapter = OpenClawAdapter(target="ws://127.0.0.1:18789")

async def main():
    # Connect
    connected = await adapter.connect()
    if not connected:
        raise RuntimeError("Failed to connect")
    
    try:
        # Send prompt
        output = await adapter.send_prompt(
            "List all files in the current directory"
        )
        
        print(f"Response: {output.response_text}")
        print(f"Tool calls: {output.tool_calls}")
        
    finally:
        await adapter.disconnect()

import asyncio
asyncio.run(main())
```

### MockAdapter

Deterministic responses for offline testing.

```python
from superclaw.adapters import MockAdapter

adapter = MockAdapter()

async def main():
    await adapter.connect()
    
    # Mock adapter returns predictable responses
    output = await adapter.send_prompt("Test prompt")
    
    print(output.response_text)  # Predictable mock response
    
    await adapter.disconnect()
```

### ACPAdapter

Communicates via Agent Communication Protocol subprocess.

```python
from superclaw.adapters import ACPAdapter

adapter = ACPAdapter(
    command="opencode acp",
    project="/path/to/project"
)

async def main():
    await adapter.connect()
    output = await adapter.send_prompt("Hello")
    await adapter.disconnect()
```

---

## Adapter Factory

Create adapters using the factory function.

```python
from superclaw.adapters import create_adapter

# OpenClaw adapter
adapter = create_adapter("openclaw", {
    "target": "ws://127.0.0.1:18789"
})

# Mock adapter
adapter = create_adapter("mock", {})

# ACP adapter
adapter = create_adapter("acp", {
    "command": "opencode acp",
    "project": "/path/to/project"
})
```

---

## Creating Custom Adapters

```python
from superclaw.adapters.base import AgentAdapter, AgentOutput, ToolCall
import httpx

class HTTPAgentAdapter(AgentAdapter):
    """Adapter for HTTP-based agents."""
    
    def __init__(self, base_url: str, api_key: str | None = None):
        self.base_url = base_url
        self.api_key = api_key
        self.client: httpx.AsyncClient | None = None
    
    async def connect(self) -> bool:
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=headers,
            timeout=30.0
        )
        
        # Verify connection
        return await self.health_check()
    
    async def disconnect(self) -> None:
        if self.client:
            await self.client.aclose()
            self.client = None
    
    async def send_prompt(
        self, 
        prompt: str, 
        context: dict | None = None
    ) -> AgentOutput:
        if not self.client:
            raise RuntimeError("Not connected")
        
        response = await self.client.post(
            "/chat",
            json={"message": prompt, **(context or {})}
        )
        response.raise_for_status()
        
        data = response.json()
        
        # Parse tool calls from response
        tool_calls = [
            ToolCall(name=tc["name"], args=tc["args"])
            for tc in data.get("tool_calls", [])
        ]
        
        return AgentOutput(
            response_text=data.get("response"),
            tool_calls=tool_calls,
            tool_results=[],
            artifacts=[],
            secrets_detected=[],
            raw_response=data,
        )
    
    async def health_check(self) -> bool:
        if not self.client:
            return False
        
        try:
            response = await self.client.get("/health")
            return response.status_code == 200
        except Exception:
            return False

# Register the adapter
from superclaw.adapters import ADAPTER_REGISTRY
ADAPTER_REGISTRY["http"] = HTTPAgentAdapter
```

---

## Using Adapters with Attacks

```python
from superclaw.adapters import create_adapter
from superclaw.attacks import run_attack

# Create custom adapter config
adapter = create_adapter("openclaw", {
    "target": "ws://127.0.0.1:18789"
})

# Run attacks using the adapter
results = run_attack(
    adapter=adapter,  # Pass adapter directly
    behaviors=["prompt-injection-resistance"],
)
```

---

## Connection Management

### Context Manager

```python
from superclaw.adapters import create_adapter

async def main():
    adapter = create_adapter("openclaw", {"target": "ws://127.0.0.1:18789"})
    
    async with adapter:  # Automatically connects/disconnects
        output = await adapter.send_prompt("Hello")
        print(output.response_text)
```

### Manual Management

```python
adapter = create_adapter("openclaw", {"target": "ws://127.0.0.1:18789"})

try:
    await adapter.connect()
    output = await adapter.send_prompt("Hello")
finally:
    await adapter.disconnect()
```

---

## See Also

- [Attacks API](attacks.md) — Attack implementations
- [Behaviors API](behaviors.md) — Security behavior specifications
