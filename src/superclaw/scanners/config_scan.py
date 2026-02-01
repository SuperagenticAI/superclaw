"""Configuration scanner for SuperClaw safety checks."""

from __future__ import annotations

from dataclasses import dataclass
from ipaddress import ip_address, ip_network
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml


PRIVATE_NETWORKS = [
    ip_network("10.0.0.0/8"),
    ip_network("172.16.0.0/12"),
    ip_network("192.168.0.0/16"),
    ip_network("127.0.0.0/8"),
    ip_network("::1/128"),
]


@dataclass
class ScanFinding:
    """Single config scan finding."""

    rule: str
    severity: str
    message: str
    remediation: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule": self.rule,
            "severity": self.severity,
            "message": self.message,
            "remediation": self.remediation,
        }


def scan_config(path: Path) -> dict[str, Any]:
    """Scan a SuperClaw config file for risky settings."""
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    findings: list[ScanFinding] = []

    target = data.get("default_target") or data.get("target")
    if target:
        findings.extend(_check_target(target))
    else:
        findings.append(
            ScanFinding(
                rule="missing_default_target",
                severity="low",
                message="No default target configured.",
                remediation="Set default_target to a local gateway URL.",
            )
        )

    safety = data.get("safety", {})
    findings.extend(_check_safety(safety))

    llm = data.get("llm", {})
    findings.extend(_check_llm(llm))

    logging = data.get("logging", {})
    findings.extend(_check_logging(logging))

    auth = data.get("auth", {})
    findings.extend(_check_auth(auth))

    summary = _summarize(findings)
    return {
        "findings": [f.to_dict() for f in findings],
        "summary": summary,
        "config_path": str(path),
    }


def _check_target(target: str) -> list[ScanFinding]:
    findings: list[ScanFinding] = []
    parsed = urlparse(target)
    host = parsed.hostname
    scheme = parsed.scheme

    if scheme not in {"ws", "wss"}:
        findings.append(
            ScanFinding(
                rule="target_scheme",
                severity="medium",
                message=f"Target scheme '{scheme}' is not ws:// or wss://.",
                remediation="Use ws:// for local testing or wss:// for remote targets.",
            )
        )

    if not host:
        findings.append(
            ScanFinding(
                rule="target_host_missing",
                severity="high",
                message="Target host is missing or invalid.",
                remediation="Set default_target to a valid host (e.g., ws://127.0.0.1:18789).",
            )
        )
        return findings

    if host in {"localhost"}:
        return findings

    if host in {"0.0.0.0", "::"}:
        findings.append(
            ScanFinding(
                rule="target_bind_all",
                severity="high",
                message=f"Target host '{host}' binds to all interfaces.",
                remediation="Bind the gateway to localhost or a private interface.",
            )
        )
        return findings

    if _is_private_ip(host):
        return findings

    findings.append(
        ScanFinding(
            rule="target_public",
            severity="high",
            message=f"Target host '{host}' appears to be public.",
            remediation="Use a VPN or bind the gateway to localhost to avoid exposure.",
        )
    )

    if scheme == "ws":
        findings.append(
            ScanFinding(
                rule="target_insecure_ws",
                severity="medium",
                message="Using ws:// with a non-local target.",
                remediation="Use wss:// for remote targets.",
            )
        )

    return findings


def _check_safety(safety: dict[str, Any]) -> list[ScanFinding]:
    findings: list[ScanFinding] = []

    require_auth = safety.get("require_authorization", True)
    if not require_auth:
        findings.append(
            ScanFinding(
                rule="require_authorization_disabled",
                severity="high",
                message="Safety.require_authorization is disabled.",
                remediation="Set safety.require_authorization to true.",
            )
        )

    local_only = safety.get("local_only", True)
    if not local_only:
        findings.append(
            ScanFinding(
                rule="local_only_disabled",
                severity="medium",
                message="Safety.local_only is disabled.",
                remediation="Set safety.local_only to true for local testing.",
            )
        )

    max_concurrent = safety.get("max_concurrent_attacks")
    if isinstance(max_concurrent, int):
        if max_concurrent <= 0:
            findings.append(
                ScanFinding(
                    rule="max_concurrent_attacks_invalid",
                    severity="medium",
                    message="Safety.max_concurrent_attacks is set to 0 or below.",
                    remediation="Set max_concurrent_attacks to a positive integer.",
                )
            )
        elif max_concurrent > 20:
            findings.append(
                ScanFinding(
                    rule="max_concurrent_attacks_high",
                    severity="low",
                    message=f"Safety.max_concurrent_attacks is high ({max_concurrent}).",
                    remediation="Reduce concurrency to avoid overwhelming targets.",
                )
            )

    return findings


def _check_llm(llm: dict[str, Any]) -> list[ScanFinding]:
    findings: list[ScanFinding] = []
    provider = str(llm.get("provider", "")).strip()
    if not provider:
        findings.append(
            ScanFinding(
                rule="llm_provider_missing",
                severity="low",
                message="LLM provider is not configured.",
                remediation="Set llm.provider to openai, anthropic, google, or ollama.",
            )
        )
    model = str(llm.get("model", "")).strip()
    if not model:
        findings.append(
            ScanFinding(
                rule="llm_model_missing",
                severity="low",
                message="LLM model is not configured.",
                remediation="Set llm.model to a valid model ID.",
            )
        )
    return findings


def _check_logging(logging: dict[str, Any]) -> list[ScanFinding]:
    findings: list[ScanFinding] = []
    level = str(logging.get("level", "INFO")).strip().upper()
    if level in {"", "OFF", "NONE"}:
        findings.append(
            ScanFinding(
                rule="logging_disabled",
                severity="low",
                message="Logging appears to be disabled.",
                remediation="Set logging.level to INFO or DEBUG during audits.",
            )
        )
    log_file = str(logging.get("file", "")).strip()
    if not log_file:
        findings.append(
            ScanFinding(
                rule="logging_file_missing",
                severity="low",
                message="Logging file path is not configured.",
                remediation="Set logging.file to a local path for audit trails.",
            )
        )
    return findings


def _check_auth(auth: dict[str, Any]) -> list[ScanFinding]:
    findings: list[ScanFinding] = []
    if auth.get("token") or auth.get("password"):
        findings.append(
            ScanFinding(
                rule="auth_secrets_in_config",
                severity="medium",
                message="Auth secrets are stored in the config file.",
                remediation="Prefer environment variables for secrets.",
            )
        )
    return findings


def _summarize(findings: list[ScanFinding]) -> dict[str, Any]:
    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for finding in findings:
        if finding.severity in severity_counts:
            severity_counts[finding.severity] += 1

    return {
        "total": len(findings),
        "severity": severity_counts,
    }


def _is_private_ip(host: str) -> bool:
    try:
        ip = ip_address(host)
    except ValueError:
        return False

    return any(ip in network for network in PRIVATE_NETWORKS)
