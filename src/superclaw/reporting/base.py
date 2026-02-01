"""Base report generator and routing logic."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class ReportGenerator(ABC):
    """Abstract base class for report generators."""

    @abstractmethod
    def generate(self, results: dict[str, Any], output: str) -> None:
        """Generate a report from audit results.

        Args:
            results: The audit results dictionary containing findings.
            output: The output file path for the generated report.
        """
        pass

    def _ensure_parent_dir(self, output: str) -> None:
        """Ensure the parent directory exists for the output file."""
        Path(output).parent.mkdir(parents=True, exist_ok=True)


def generate_report(results: dict[str, Any], format: str, output: str) -> None:
    """Generate a report in the specified format.

    Args:
        results: The audit results dictionary containing findings.
        format: The output format ('html', 'json', 'sarif').
        output: The output file path for the generated report.

    Raises:
        ValueError: If the format is not supported.
    """
    from superclaw.reporting.html import HTMLReportGenerator
    from superclaw.reporting.json_report import JSONReportGenerator
    from superclaw.reporting.sarif import SARIFReportGenerator

    generators: dict[str, type[ReportGenerator]] = {
        "html": HTMLReportGenerator,
        "json": JSONReportGenerator,
        "sarif": SARIFReportGenerator,
    }

    format_lower = format.lower()
    if format_lower not in generators:
        raise ValueError(
            f"Unsupported report format: {format}. "
            f"Supported formats: {', '.join(generators.keys())}"
        )

    generator = generators[format_lower]()
    generator.generate(results, output)
