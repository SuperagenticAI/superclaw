"""SuperClaw settings management."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class Settings:
    """SuperClaw configuration settings."""

    target: str = "ws://127.0.0.1:18789"
    agent_type: str = "openclaw"
    behaviors: list[str] = field(default_factory=list)
    techniques: list[str] = field(default_factory=list)
    output_format: str = "json"
    log_level: str = "INFO"
    safety_require_authorization: bool = True
    safety_local_only: bool = True
    safety_max_concurrent_attacks: int = 5

    @classmethod
    def from_dict(cls, data: dict) -> Settings:
        """Create Settings from a dictionary."""
        safety = data.get("safety", {}) or {}
        return cls(
            target=data.get("default_target", data.get("target", cls.target)),
            agent_type=data.get("agent_type", cls.agent_type),
            behaviors=data.get("behaviors", []),
            techniques=data.get("techniques", []),
            output_format=data.get("output_format", cls.output_format),
            log_level=data.get("logging", {}).get("level", data.get("log_level", cls.log_level)),
            safety_require_authorization=bool(safety.get("require_authorization", True)),
            safety_local_only=bool(safety.get("local_only", True)),
            safety_max_concurrent_attacks=int(safety.get("max_concurrent_attacks", 5)),
        )

    @classmethod
    def from_file(cls, path: Path) -> Settings:
        """Load settings from a YAML file."""
        with open(path) as f:
            data = yaml.safe_load(f) or {}
        return cls.from_dict(data)


_settings: Settings | None = None


def get_settings() -> Settings:
    """Get settings from environment or config file.

    Priority:
    1. Environment variables (SUPERCLAW_*)
    2. Config file (~/.superclaw/config.yaml)
    3. Defaults
    """
    global _settings

    if _settings is not None:
        return _settings

    settings = Settings()

    config_file = Path.home() / ".superclaw" / "config.yaml"
    if config_file.exists():
        settings = Settings.from_file(config_file)

    if target := os.environ.get("SUPERCLAW_TARGET"):
        settings.target = target
    if agent_type := os.environ.get("SUPERCLAW_AGENT_TYPE"):
        settings.agent_type = agent_type
    if behaviors := os.environ.get("SUPERCLAW_BEHAVIORS"):
        settings.behaviors = behaviors.split(",")
    if techniques := os.environ.get("SUPERCLAW_TECHNIQUES"):
        settings.techniques = techniques.split(",")
    if output_format := os.environ.get("SUPERCLAW_OUTPUT_FORMAT"):
        settings.output_format = output_format
    if log_level := os.environ.get("SUPERCLAW_LOG_LEVEL"):
        settings.log_level = log_level
    if require_auth := os.environ.get("SUPERCLAW_REQUIRE_AUTH"):
        settings.safety_require_authorization = require_auth.lower() in {"1", "true", "yes"}
    if local_only := os.environ.get("SUPERCLAW_LOCAL_ONLY"):
        settings.safety_local_only = local_only.lower() in {"1", "true", "yes"}
    if max_concurrent := os.environ.get("SUPERCLAW_MAX_CONCURRENT_ATTACKS"):
        try:
            settings.safety_max_concurrent_attacks = int(max_concurrent)
        except ValueError:
            pass

    _settings = settings
    return settings
