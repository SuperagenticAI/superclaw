"""SARIF 2.1.0 report generator for CI/CD integration."""

import json
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from superclaw.reporting.base import ReportGenerator


class SARIFReportGenerator(ReportGenerator):
    """Generates SARIF 2.1.0 format reports for GitHub Code Scanning integration."""

    SARIF_VERSION = "2.1.0"
    SARIF_SCHEMA = "https://json.schemastore.org/sarif-2.1.0.json"
    TOOL_NAME = "superclaw"
    TOOL_VERSION = "1.0.0"

    SEVERITY_TO_LEVEL: dict[str, str] = {
        "critical": "error",
        "high": "error",
        "medium": "warning",
        "low": "note",
    }

    SEVERITY_TO_SECURITY_SEVERITY: dict[str, str] = {
        "critical": "9.0",
        "high": "7.0",
        "medium": "5.0",
        "low": "3.0",
    }

    def generate(self, results: dict[str, Any], output: str) -> None:
        """Generate a SARIF report from audit results.

        Args:
            results: The audit results dictionary containing findings.
            output: The output file path for the generated report.
        """
        self._ensure_parent_dir(output)

        sarif = self._build_sarif(results)

        with open(output, "w", encoding="utf-8") as f:
            json.dump(sarif, f, indent=2)

    def _build_sarif(self, results: dict[str, Any]) -> dict[str, Any]:
        """Build the complete SARIF document."""
        findings = results.get("findings", results.get("results", []))
        if not isinstance(findings, list):
            findings = []

        rules = self._build_rules(findings)
        sarif_results = self._build_results(findings)

        return {
            "$schema": self.SARIF_SCHEMA,
            "version": self.SARIF_VERSION,
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": self.TOOL_NAME,
                            "version": self.TOOL_VERSION,
                            "informationUri": "https://github.com/superagentic/superclaw",
                            "rules": rules,
                        }
                    },
                    "results": sarif_results,
                    "invocations": [
                        {
                            "executionSuccessful": True,
                            "endTimeUtc": datetime.now(UTC).isoformat(),
                        }
                    ],
                    "automationDetails": {
                        "id": f"superclaw-audit-{uuid4().hex[:8]}",
                        "description": {"text": "AI Agent Security Audit"},
                    },
                }
            ],
        }

    def _build_rules(self, findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Build SARIF rule definitions from findings."""
        rules: dict[str, dict[str, Any]] = {}

        for finding in findings:
            behavior = finding.get("behavior", "unknown")
            rule_id = self._behavior_to_rule_id(behavior)

            if rule_id not in rules:
                severity = finding.get("severity", "medium").lower()
                rules[rule_id] = {
                    "id": rule_id,
                    "name": self._behavior_to_name(behavior),
                    "shortDescription": {"text": str(behavior)},
                    "fullDescription": {"text": finding.get("description", str(behavior))},
                    "defaultConfiguration": {
                        "level": self.SEVERITY_TO_LEVEL.get(severity, "warning")
                    },
                    "properties": {
                        "security-severity": self.SEVERITY_TO_SECURITY_SEVERITY.get(
                            severity, "5.0"
                        ),
                        "tags": ["security", "ai-agent", f"severity-{severity}"],
                    },
                    "helpUri": "https://github.com/superagentic/superclaw#behaviors",
                }

        return list(rules.values())

    def _build_results(self, findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Build SARIF results from findings."""
        sarif_results = []

        for finding in findings:
            if finding.get("status") != "failed":
                continue

            behavior = finding.get("behavior", "unknown")
            severity = finding.get("severity", "medium").lower()
            evidence = finding.get("evidence", "")

            result = {
                "ruleId": self._behavior_to_rule_id(behavior),
                "level": self.SEVERITY_TO_LEVEL.get(severity, "warning"),
                "message": {"text": self._build_message(finding)},
                "locations": self._build_locations(finding),
                "fingerprints": {"primaryLocationLineHash": uuid4().hex},
            }

            if evidence:
                result["properties"] = {
                    "evidence": str(evidence)[:1000],
                }

            sarif_results.append(result)

        return sarif_results

    def _build_message(self, finding: dict[str, Any]) -> str:
        """Build a descriptive message for a finding."""
        behavior = finding.get("behavior", "Unknown behavior")
        evidence = finding.get("evidence", "")

        message = f"Security behavior violation: {behavior}"
        if evidence:
            message += f"\n\nEvidence: {evidence[:500]}"

        return message

    def _build_locations(self, finding: dict[str, Any]) -> list[dict[str, Any]]:
        """Build SARIF locations from a finding."""
        location = finding.get("location", {})
        file_path = location.get("file", finding.get("file", "agent-interaction"))
        line = location.get("line", finding.get("line", 1))

        return [
            {
                "physicalLocation": {
                    "artifactLocation": {
                        "uri": file_path,
                        "uriBaseId": "%SRCROOT%",
                    },
                    "region": {
                        "startLine": max(
                            1,
                            int(line)
                            if isinstance(line, int | str) and str(line).isdigit()
                            else 1,
                        ),
                    },
                }
            }
        ]

    def _behavior_to_rule_id(self, behavior: str) -> str:
        """Convert a behavior string to a SARIF rule ID."""
        clean = str(behavior).lower()
        clean = "".join(c if c.isalnum() or c in "-_" else "-" for c in clean)
        clean = "-".join(filter(None, clean.split("-")))
        return f"superclaw/{clean[:50]}"

    def _behavior_to_name(self, behavior: str) -> str:
        """Convert a behavior string to a readable rule name."""
        return str(behavior).replace("_", " ").replace("-", " ").title()[:100]
