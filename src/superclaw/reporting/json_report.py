"""JSON report generator for security audit results."""

import json
from datetime import UTC, datetime
from typing import Any

from superclaw.reporting.base import ReportGenerator


class JSONReportGenerator(ReportGenerator):
    """Generates JSON format security audit reports."""

    VERSION = "1.0.0"

    def generate(self, results: dict[str, Any], output: str) -> None:
        """Generate a JSON report from audit results.

        Args:
            results: The audit results dictionary containing findings.
            output: The output file path for the generated report.
        """
        self._ensure_parent_dir(output)

        report = self._build_report(results)

        with open(output, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, default=str)

    def _build_report(self, results: dict[str, Any]) -> dict[str, Any]:
        """Build the complete JSON report structure."""
        return {
            "metadata": self._build_metadata(results),
            "summary": self._build_summary(results),
            "findings": results.get("findings", results.get("results", [])),
            "scenarios": results.get("scenarios", []),
        }

    def _build_metadata(self, results: dict[str, Any]) -> dict[str, Any]:
        """Build the metadata section of the report."""
        return {
            "version": self.VERSION,
            "timestamp": datetime.now(UTC).isoformat(),
            "generator": "superclaw",
            "agent_type": results.get("agent_type", "unknown"),
            "target": results.get("target", "unknown"),
            "config": results.get("config", {}),
        }

    def _build_summary(self, results: dict[str, Any]) -> dict[str, Any]:
        """Build the summary section with statistics."""
        findings = results.get("findings", results.get("results", []))

        if not isinstance(findings, list):
            findings = []

        passed = sum(1 for f in findings if f.get("status") == "passed")
        failed = sum(1 for f in findings if f.get("status") == "failed")
        skipped = sum(1 for f in findings if f.get("status") == "skipped")

        severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for f in findings:
            if f.get("status") == "failed":
                severity = f.get("severity", "medium").lower()
                if severity in severity_counts:
                    severity_counts[severity] += 1

        return {
            "total": len(findings),
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "pass_rate": round(passed / len(findings) * 100, 2) if findings else 0,
            "severity_breakdown": severity_counts,
        }
