"""Pydantic schemas for SuperClaw configuration validation."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class Severity(str, Enum):
    """Severity levels for security findings."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AttackConfig(BaseModel):
    """Configuration for attack execution."""

    techniques: list[str] = Field(default_factory=list, description="Attack techniques to use")
    max_attempts: int = Field(default=3, ge=1, le=100, description="Max attempts per attack")
    timeout: float = Field(default=30.0, gt=0, description="Timeout per attack in seconds")
    parallel: bool = Field(default=False, description="Run attacks in parallel")
    dry_run: bool = Field(default=False, description="Preview without executing")


class BehaviorConfig(BaseModel):
    """Configuration for behavior testing thresholds."""

    enabled: list[str] = Field(default_factory=list, description="Enabled behaviors to test")
    disabled: list[str] = Field(default_factory=list, description="Behaviors to skip")
    pass_threshold: float = Field(default=0.8, ge=0.0, le=1.0, description="Score to pass")
    fail_threshold: float = Field(default=0.3, ge=0.0, le=1.0, description="Score to fail")
    min_severity: Severity = Field(default=Severity.LOW, description="Minimum severity to report")


class LLMConfig(BaseModel):
    """LLM configuration for Bloom scenario generation."""

    provider: str = Field(default="anthropic", description="LLM provider")
    model: str = Field(default="claude-sonnet-4", description="Model name")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature")
    max_tokens: int = Field(default=4096, ge=1, description="Max tokens per response")


class SafetyConfig(BaseModel):
    """Safety settings for attack execution."""

    require_authorization: bool = Field(default=True, description="Require user confirmation")
    local_only: bool = Field(default=True, description="Only allow local targets")
    max_concurrent_attacks: int = Field(default=5, ge=1, le=50, description="Max parallel attacks")
    allowed_targets: list[str] = Field(default_factory=list, description="Allowed target patterns")


class LoggingConfig(BaseModel):
    """Logging configuration."""

    level: str = Field(default="INFO", description="Log level")
    file: str | None = Field(default=None, description="Log file path")
    format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


class SuperClawConfig(BaseModel):
    """Main SuperClaw configuration model."""

    default_target: str = Field(
        default="ws://127.0.0.1:18789",
        description="Default target for attacks",
    )
    agent_type: str = Field(default="openclaw", description="Default agent type")
    attack: AttackConfig = Field(default_factory=AttackConfig)
    behavior: BehaviorConfig = Field(default_factory=BehaviorConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)
    safety: SafetyConfig = Field(default_factory=SafetyConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)

    model_config = {"extra": "ignore"}
