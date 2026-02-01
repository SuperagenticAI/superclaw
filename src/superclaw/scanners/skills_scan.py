"""Supply-chain scanner for skills/plugins."""

from __future__ import annotations

import json
import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SUSPICIOUS_JS_PATTERNS = [
    (
        re.compile(r"\bchild_process\.(exec|execSync|spawn|spawnSync)\b"),
        "exec_child_process",
        "medium",
    ),
    (re.compile(r"\beval\("), "eval_usage", "medium"),
    (re.compile(r"\bFunction\("), "function_constructor", "medium"),
    (re.compile(r"\bprocess\.env\b"), "env_access", "low"),
]

SUSPICIOUS_PY_PATTERNS = [
    (re.compile(r"\bos\.system\("), "os_system", "medium"),
    (re.compile(r"\bsubprocess\."), "subprocess_usage", "medium"),
    (re.compile(r"\beval\("), "eval_usage", "medium"),
    (re.compile(r"\bexec\("), "exec_usage", "medium"),
    (re.compile(r"\bbase64\.b64decode\("), "base64_decode", "low"),
]

SUSPICIOUS_SHELL_PATTERNS = [
    (re.compile(r"\bcurl\b"), "curl_usage", "low"),
    (re.compile(r"\bwget\b"), "wget_usage", "low"),
    (re.compile(r"\bnc\b"), "netcat_usage", "medium"),
    (re.compile(r"\bbash\s+-c\b"), "bash_c", "medium"),
]


@dataclass
class SupplyChainFinding:
    """Single supply-chain scan finding."""

    rule: str
    severity: str
    message: str
    file: str | None = None
    line: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule": self.rule,
            "severity": self.severity,
            "message": self.message,
            "file": self.file,
            "line": self.line,
        }


def scan_skills(path: Path) -> dict[str, Any]:
    """Scan a skills/plugins directory for supply-chain risks."""
    if not path.exists():
        raise FileNotFoundError(f"Path not found: {path}")

    findings: list[SupplyChainFinding] = []

    for pkg_json in path.rglob("package.json"):
        findings.extend(_scan_package_json(pkg_json))

    for file_path in _iter_source_files(path):
        findings.extend(_scan_source_file(file_path))

    summary = _summarize(findings)
    return {
        "findings": [f.to_dict() for f in findings],
        "summary": summary,
        "scan_path": str(path),
    }


def _scan_package_json(path: Path) -> list[SupplyChainFinding]:
    findings: list[SupplyChainFinding] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return findings

    scripts = data.get("scripts", {}) if isinstance(data, dict) else {}
    if not isinstance(scripts, dict):
        return findings

    for script_name in ("preinstall", "install", "postinstall", "prepare"):
        if script_name in scripts:
            findings.append(
                SupplyChainFinding(
                    rule="npm_install_script",
                    severity="high",
                    message=(
                        f"package.json defines '{script_name}' script: {scripts.get(script_name)}"
                    ),
                    file=str(path),
                    line=None,
                )
            )

    return findings


def _iter_source_files(path: Path) -> Iterable[Path]:
    suffixes = {".py", ".js", ".ts", ".sh"}
    for file_path in path.rglob("*"):
        if file_path.is_file() and file_path.suffix in suffixes:
            yield file_path


def _scan_source_file(path: Path) -> list[SupplyChainFinding]:
    findings: list[SupplyChainFinding] = []
    try:
        content = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception:
        return findings

    if path.suffix in {".js", ".ts"}:
        patterns = SUSPICIOUS_JS_PATTERNS
    elif path.suffix == ".py":
        patterns = SUSPICIOUS_PY_PATTERNS
    else:
        patterns = SUSPICIOUS_SHELL_PATTERNS

    for idx, line in enumerate(content, start=1):
        for regex, rule, severity in patterns:
            if regex.search(line):
                findings.append(
                    SupplyChainFinding(
                        rule=rule,
                        severity=severity,
                        message=f"Suspicious pattern '{rule}' found",
                        file=str(path),
                        line=idx,
                    )
                )

    return findings


def _summarize(findings: list[SupplyChainFinding]) -> dict[str, Any]:
    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for finding in findings:
        if finding.severity in severity_counts:
            severity_counts[finding.severity] += 1

    return {
        "total": len(findings),
        "severity": severity_counts,
    }
