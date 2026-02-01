"""SuperClaw CLI - Agent Security Testing Framework."""

from __future__ import annotations

import json
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

app = typer.Typer(
    name="superclaw",
    help="🦞 SuperClaw - Break AI coding agents with style",
    no_args_is_help=True,
)
console = Console()
error_console = Console(stderr=True)

# Sub-command groups
attack_app = typer.Typer(help="Attack AI agents")
generate_app = typer.Typer(help="Generate attack scenarios")
evaluate_app = typer.Typer(help="Evaluate agent security")
audit_app = typer.Typer(help="Run security audits")
report_app = typer.Typer(help="Generate reports")
codeoptix_app = typer.Typer(help="CodeOptiX integration")
scan_app = typer.Typer(help="Scan configurations and environments")

app.add_typer(attack_app, name="attack")
app.add_typer(generate_app, name="generate")
app.add_typer(evaluate_app, name="evaluate")
app.add_typer(audit_app, name="audit")
app.add_typer(report_app, name="report")
app.add_typer(codeoptix_app, name="codeoptix")
app.add_typer(scan_app, name="scan")


def handle_error(message: str, exception: Exception | None = None) -> None:
    """Display error message and exit."""
    error_console.print(f"[bold red]Error:[/bold red] {message}")
    if exception:
        error_console.print(f"[dim]{type(exception).__name__}: {exception}[/dim]")
    raise typer.Exit(code=1)


# ============================================================
# ATTACK COMMANDS
# ============================================================


@attack_app.command("openclaw")
def attack_openclaw(
    target: str = typer.Option(
        "ws://127.0.0.1:18789",
        "--target", "-t",
        help="OpenClaw gateway URL"
    ),
    behaviors: str = typer.Option(
        "all",
        "--behaviors", "-b",
        help="Comma-separated behaviors to test"
    ),
    techniques: str = typer.Option(
        "all",
        "--techniques",
        help="Attack techniques to use"
    ),
    output: str | None = typer.Option(
        None,
        "--output", "-o",
        help="Output file for results"
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show what would be done without executing"
    ),
):
    """Attack an OpenClaw agent."""
    console.print(Panel.fit(
        "[bold red]🦞 SuperClaw[/bold red] attacking [bold cyan]OpenClaw[/bold cyan]",
        border_style="red"
    ))
    console.print(f"  Target: [cyan]{target}[/cyan]")
    console.print(f"  Behaviors: [yellow]{behaviors}[/yellow]")
    console.print(f"  Techniques: [yellow]{techniques}[/yellow]")
    console.print()

    if dry_run:
        console.print("[dim]Dry run mode - no attacks executed[/dim]")
        return

    try:
        from superclaw.attacks import run_attack

        behavior_list = behaviors.split(",") if behaviors != "all" else None
        technique_list = techniques.split(",") if techniques != "all" else None

        results = run_attack(
            agent_type="openclaw",
            target=target,
            behaviors=behavior_list,
            techniques=technique_list,
        )

        _display_attack_results(results)

        if output:
            with open(output, "w") as f:
                json.dump(results, f, indent=2, default=str)
            console.print(f"\n[green]✓ Results saved to {output}[/green]")
    except ConnectionError as e:
        handle_error(f"Failed to connect to target: {target}", e)
    except Exception as e:
        handle_error("Attack failed", e)


@attack_app.command("acp")
def attack_acp(
    command: str = typer.Option(
        ...,
        "--command", "-c",
        help="ACP agent command (e.g., 'opencode acp')"
    ),
    project: str = typer.Option(
        ".",
        "--project", "-p",
        help="Project directory"
    ),
    behaviors: str = typer.Option(
        "all",
        "--behaviors", "-b",
        help="Comma-separated behaviors"
    ),
    output: str | None = typer.Option(
        None,
        "--output", "-o",
        help="Output file"
    ),
):
    """Attack any ACP-compatible agent."""
    console.print(Panel.fit(
        "[bold red]🦞 SuperClaw[/bold red] attacking [bold cyan]ACP Agent[/bold cyan]",
        border_style="red"
    ))
    console.print(f"  Command: [cyan]{command}[/cyan]")
    console.print(f"  Project: [yellow]{project}[/yellow]")
    console.print(f"  Behaviors: [yellow]{behaviors}[/yellow]")
    console.print()

    try:
        from superclaw.attacks import run_attack

        behavior_list = behaviors.split(",") if behaviors != "all" else None

        results = run_attack(
            agent_type="acp",
            target=command,
            project_dir=project,
            behaviors=behavior_list,
        )

        _display_attack_results(results)

        if output:
            with open(output, "w") as f:
                json.dump(results, f, indent=2, default=str)
            console.print(f"\n[green]✓ Results saved to {output}[/green]")
    except Exception as e:
        handle_error("ACP attack failed", e)


@attack_app.command("mock")
def attack_mock(
    mock_response: list[str] = typer.Option(
        [],
        "--mock-response",
        help="Mock response text (can be provided multiple times)"
    ),
    echo_prompt: bool = typer.Option(
        False,
        "--echo-prompt",
        help="Append the prompt to the mock response"
    ),
    simulate_injection: bool = typer.Option(
        False,
        "--simulate-injection",
        help="Simulate a successful injection attempt"
    ),
    behaviors: str = typer.Option(
        "all",
        "--behaviors", "-b",
        help="Comma-separated behaviors to test"
    ),
    techniques: str = typer.Option(
        "all",
        "--techniques",
        help="Attack techniques to use"
    ),
    output: str | None = typer.Option(
        None,
        "--output", "-o",
        help="Output file for results"
    ),
):
    """Attack a mock agent (offline testing)."""
    console.print(Panel.fit(
        "[bold red]🦞 SuperClaw[/bold red] attacking [bold cyan]Mock Agent[/bold cyan]",
        border_style="red"
    ))
    console.print(f"  Behaviors: [yellow]{behaviors}[/yellow]")
    console.print(f"  Techniques: [yellow]{techniques}[/yellow]")
    console.print()

    try:
        from superclaw.attacks import run_attack

        behavior_list = behaviors.split(",") if behaviors != "all" else None
        technique_list = techniques.split(",") if techniques != "all" else None
        adapter_config = {
            "responses": mock_response or ["Mock response"],
            "echo_prompt": echo_prompt,
            "simulate_injection": simulate_injection,
        }

        results = run_attack(
            agent_type="mock",
            target="mock",
            behaviors=behavior_list,
            techniques=technique_list,
            adapter_config=adapter_config,
        )

        _display_attack_results(results)

        if output:
            with open(output, "w") as f:
                json.dump(results, f, indent=2, default=str)
            console.print(f"\n[green]✓ Results saved to {output}[/green]")
    except Exception as e:
        handle_error("Mock attack failed", e)


# ============================================================
# GENERATE COMMANDS (Bloom)
# ============================================================


@generate_app.command("scenarios")
def generate_scenarios(
    behavior: str = typer.Option(
        ...,
        "--behavior", "-b",
        help="Target behavior (e.g., prompt-injection-vulnerability)"
    ),
    num_scenarios: int = typer.Option(
        10,
        "--num-scenarios", "-n",
        help="Number of scenarios to generate"
    ),
    variations: str = typer.Option(
        "noise,emotional_pressure",
        "--variations", "-v",
        help="Variation dimensions (comma-separated)"
    ),
    output: str = typer.Option(
        "scenarios.json",
        "--output", "-o",
        help="Output file"
    ),
    model: str = typer.Option(
        "claude-sonnet-4",
        "--model", "-m",
        help="Model for scenario generation"
    ),
):
    """Generate attack scenarios using Bloom ideation."""
    console.print(Panel.fit(
        "[bold cyan]🌸 Bloom Scenario Generation[/bold cyan]",
        border_style="cyan"
    ))
    console.print(f"  Behavior: [yellow]{behavior}[/yellow]")
    console.print(f"  Scenarios: [cyan]{num_scenarios}[/cyan]")
    console.print(f"  Variations: [yellow]{variations}[/yellow]")
    console.print(f"  Model: [dim]{model}[/dim]")
    console.print()

    try:
        from superclaw.bloom import generate_scenarios as gen_scenarios

        variation_list = variations.split(",") if variations else []

        with console.status("[cyan]Generating scenarios...[/cyan]"):
            scenarios = gen_scenarios(
                behavior=behavior,
                num_scenarios=num_scenarios,
                variation_dimensions=variation_list,
                model=model,
            )

        console.print(f"[green]✓ Generated {len(scenarios)} scenarios[/green]")

        with open(output, "w") as f:
            json.dump(scenarios, f, indent=2)
        console.print(f"[green]✓ Saved to {output}[/green]")
    except Exception as e:
        handle_error("Scenario generation failed", e)


# ============================================================
# EVALUATE COMMANDS
# ============================================================


@evaluate_app.command("openclaw")
def evaluate_openclaw(
    target: str = typer.Option(
        "ws://127.0.0.1:18789",
        "--target", "-t",
        help="OpenClaw gateway URL"
    ),
    scenarios: str | None = typer.Option(
        None,
        "--scenarios", "-s",
        help="Scenarios JSON file"
    ),
    behaviors: str = typer.Option(
        "all",
        "--behaviors", "-b",
        help="Behaviors to evaluate"
    ),
    techniques: str = typer.Option(
        "all",
        "--techniques",
        help="Attack techniques to use"
    ),
    output: str | None = typer.Option(
        None,
        "--output", "-o",
        help="Output file"
    ),
):
    """Evaluate OpenClaw agent against security behaviors."""
    console.print(Panel.fit(
        "[bold yellow]🔍 SuperClaw Evaluation[/bold yellow]",
        border_style="yellow"
    ))
    console.print(f"  Target: [cyan]{target}[/cyan]")
    console.print(f"  Behaviors: [yellow]{behaviors}[/yellow]")
    console.print(f"  Techniques: [yellow]{techniques}[/yellow]")
    if scenarios:
        console.print(f"  Scenarios: [dim]{scenarios}[/dim]")
    console.print()

    try:
        from superclaw.attacks import run_evaluation

        scenario_data = None
        if scenarios:
            if not Path(scenarios).exists():
                handle_error(f"Scenarios file not found: {scenarios}")
            with open(scenarios) as f:
                scenario_data = json.load(f)

        behavior_list = behaviors.split(",") if behaviors != "all" else None
        technique_list = techniques.split(",") if techniques != "all" else None

        results = run_evaluation(
            agent_type="openclaw",
            target=target,
            scenarios=scenario_data,
            behaviors=behavior_list,
            techniques=technique_list,
        )

        _display_evaluation_results(results)

        if output:
            with open(output, "w") as f:
                json.dump(results, f, indent=2, default=str)
            console.print(f"\n[green]✓ Results saved to {output}[/green]")
    except json.JSONDecodeError as e:
        handle_error(f"Invalid JSON in scenarios file: {scenarios}", e)
    except Exception as e:
        handle_error("Evaluation failed", e)


@evaluate_app.command("mock")
def evaluate_mock(
    mock_response: list[str] = typer.Option(
        [],
        "--mock-response",
        help="Mock response text (can be provided multiple times)"
    ),
    echo_prompt: bool = typer.Option(
        False,
        "--echo-prompt",
        help="Append the prompt to the mock response"
    ),
    simulate_injection: bool = typer.Option(
        False,
        "--simulate-injection",
        help="Simulate a successful injection attempt"
    ),
    scenarios: str | None = typer.Option(
        None,
        "--scenarios", "-s",
        help="Scenarios JSON file"
    ),
    behaviors: str = typer.Option(
        "all",
        "--behaviors", "-b",
        help="Behaviors to evaluate"
    ),
    output: str | None = typer.Option(
        None,
        "--output", "-o",
        help="Output file"
    ),
):
    """Evaluate a mock agent (offline testing)."""
    console.print(Panel.fit(
        "[bold yellow]🔍 SuperClaw Evaluation[/bold yellow]",
        border_style="yellow"
    ))
    console.print(f"  Behaviors: [yellow]{behaviors}[/yellow]")
    if scenarios:
        console.print(f"  Scenarios: [dim]{scenarios}[/dim]")
    console.print()

    try:
        from superclaw.attacks import run_evaluation

        scenario_data = None
        if scenarios:
            if not Path(scenarios).exists():
                handle_error(f"Scenarios file not found: {scenarios}")
            with open(scenarios) as f:
                scenario_data = json.load(f)

        behavior_list = behaviors.split(",") if behaviors != "all" else None
        adapter_config = {
            "responses": mock_response or ["Mock response"],
            "echo_prompt": echo_prompt,
            "simulate_injection": simulate_injection,
        }

        results = run_evaluation(
            agent_type="mock",
            target="mock",
            scenarios=scenario_data,
            behaviors=behavior_list,
            adapter_config=adapter_config,
        )

        _display_evaluation_results(results)

        if output:
            with open(output, "w") as f:
                json.dump(results, f, indent=2, default=str)
            console.print(f"\n[green]✓ Results saved to {output}[/green]")
    except json.JSONDecodeError as e:
        handle_error(f"Invalid JSON in scenarios file: {scenarios}", e)
    except Exception as e:
        handle_error("Mock evaluation failed", e)


# ============================================================
# AUDIT COMMANDS
# ============================================================


@audit_app.command("openclaw")
def audit_openclaw(
    target: str = typer.Option(
        "ws://127.0.0.1:18789",
        "--target", "-t",
        help="OpenClaw gateway URL"
    ),
    comprehensive: bool = typer.Option(
        False,
        "--comprehensive",
        help="Run comprehensive audit (all behaviors, all techniques)"
    ),
    quick: bool = typer.Option(
        False,
        "--quick",
        help="Quick security check (essential behaviors only)"
    ),
    report_format: str = typer.Option(
        "html",
        "--report-format", "-f",
        help="Report format: html, json, sarif"
    ),
    output: str = typer.Option(
        "audit-report",
        "--output", "-o",
        help="Output file (without extension)"
    ),
):
    """Run security audit on OpenClaw agent."""
    mode = "comprehensive" if comprehensive else "quick" if quick else "standard"

    console.print(Panel.fit(
        f"[bold yellow]🔍 SuperClaw Security Audit[/bold yellow] ({mode})",
        border_style="yellow"
    ))
    console.print(f"  Target: [cyan]{target}[/cyan]")
    console.print(f"  Mode: [yellow]{mode}[/yellow]")
    console.print(f"  Format: [dim]{report_format}[/dim]")
    console.print()

    try:
        from superclaw.attacks import run_audit
        from superclaw.reporting import generate_report

        with console.status(f"[yellow]Running {mode} audit...[/yellow]"):
            results = run_audit(
                agent_type="openclaw",
                target=target,
                mode=mode,
            )

        _display_audit_summary(results)

        output_file = f"{output}.{report_format}"
        generate_report(results, format=report_format, output=output_file)
        console.print(f"\n[green]✓ Report saved to {output_file}[/green]")
    except ConnectionError as e:
        handle_error(f"Failed to connect to target: {target}", e)
    except Exception as e:
        handle_error("Audit failed", e)


# ============================================================
# REPORT COMMANDS
# ============================================================


@report_app.command("generate")
def report_generate(
    results_file: str = typer.Option(
        ...,
        "--results", "-r",
        help="Results JSON file from attack/evaluate/audit"
    ),
    report_format: str = typer.Option(
        "html",
        "--format", "-f",
        help="Report format: html, json, sarif"
    ),
    output: str = typer.Option(
        "report",
        "--output", "-o",
        help="Output file (without extension)"
    ),
):
    """Generate a report from attack/evaluation results."""
    console.print(Panel.fit(
        "[bold cyan]📊 Report Generation[/bold cyan]",
        border_style="cyan"
    ))
    console.print(f"  Results: [dim]{results_file}[/dim]")
    console.print(f"  Format: [yellow]{report_format}[/yellow]")
    console.print()

    try:
        if not Path(results_file).exists():
            handle_error(f"Results file not found: {results_file}")

        with open(results_file) as f:
            results = json.load(f)

        from superclaw.reporting import generate_report

        output_file = f"{output}.{report_format}"
        generate_report(results, format=report_format, output=output_file)
        console.print(f"[green]✓ Report saved to {output_file}[/green]")
    except json.JSONDecodeError as e:
        handle_error(f"Invalid JSON in results file: {results_file}", e)
    except Exception as e:
        handle_error("Report generation failed", e)


@report_app.command("drift")
def report_drift(
    baseline: str = typer.Option(
        ...,
        "--baseline", "-b",
        help="Baseline results JSON file"
    ),
    current: str = typer.Option(
        ...,
        "--current", "-c",
        help="Current results JSON file"
    ),
    score_drop_threshold: float = typer.Option(
        0.1,
        "--score-drop-threshold",
        help="Score drop threshold to flag regression"
    ),
    output: str | None = typer.Option(
        None,
        "--output", "-o",
        help="Write JSON drift report to file"
    ),
):
    """Compare two runs and report drift."""
    console.print(Panel.fit(
        "[bold cyan]📈 SuperClaw Drift Report[/bold cyan]",
        border_style="cyan"
    ))
    console.print(f"  Baseline: [dim]{baseline}[/dim]")
    console.print(f"  Current: [dim]{current}[/dim]")
    console.print()

    try:
        if not Path(baseline).exists():
            handle_error(f"Baseline file not found: {baseline}")
        if not Path(current).exists():
            handle_error(f"Current file not found: {current}")

        with open(baseline) as f:
            baseline_data = json.load(f)
        with open(current) as f:
            current_data = json.load(f)

        from superclaw.analysis import DriftConfig, compare_runs

        drift = compare_runs(
            baseline_data,
            current_data,
            config=DriftConfig(score_drop_threshold=score_drop_threshold),
        )

        summary = drift.get("summary", {})
        console.print(
            f"[bold]Regressions:[/bold] {summary.get('regressions', 0)} | "
            f"Improvements: {summary.get('improvements', 0)}"
        )

        table = Table(title="Behavior Drift", border_style="cyan")
        table.add_column("Behavior", style="cyan")
        table.add_column("Baseline", style="white")
        table.add_column("Current", style="white")
        table.add_column("Δ", style="yellow")
        table.add_column("Change", style="red")

        for diff in drift.get("behavior_diffs", []):
            table.add_row(
                str(diff.get("behavior", "")),
                f"{diff.get('baseline_score', 0.0):.2f}",
                f"{diff.get('current_score', 0.0):.2f}",
                f"{diff.get('delta', 0.0):.2f}",
                str(diff.get("status_change", "")),
            )

        console.print(table)

        if output:
            with open(output, "w") as f:
                json.dump(drift, f, indent=2, default=str)
            console.print(f"\n[green]✓ Drift report saved to {output}[/green]")
    except json.JSONDecodeError as e:
        handle_error("Invalid JSON in results file", e)
    except Exception as e:
        handle_error("Drift report failed", e)


# ============================================================
# UTILITY COMMANDS
# ============================================================


# ============================================================
# SCAN COMMANDS
# ============================================================


@scan_app.command("config")
def scan_config(
    config: str = typer.Option(
        str(Path.home() / ".superclaw" / "config.yaml"),
        "--config", "-c",
        help="Path to superclaw config file"
    ),
    output: str | None = typer.Option(
        None,
        "--output", "-o",
        help="Write JSON results to file"
    ),
):
    """Scan SuperClaw config for risky settings."""
    console.print(Panel.fit(
        "[bold cyan]🔍 SuperClaw Config Scan[/bold cyan]",
        border_style="cyan"
    ))
    console.print(f"  Config: [dim]{config}[/dim]")
    console.print()

    try:
        from superclaw.scanners import scan_config as run_scan

        results = run_scan(Path(config))

        summary = results.get("summary", {})
        table = Table(title="Scan Findings", border_style="cyan")
        table.add_column("Rule", style="cyan")
        table.add_column("Severity", style="yellow")
        table.add_column("Message", style="white")
        table.add_column("Remediation", style="green")

        findings = results.get("findings", [])
        for finding in findings:
            table.add_row(
                str(finding.get("rule", "")),
                str(finding.get("severity", "")),
                str(finding.get("message", "")),
                str(finding.get("remediation", "")),
            )

        console.print(table)
        console.print(
            f"\n[bold]Total:[/bold] {summary.get('total', 0)} | "
            f"Critical: {summary.get('severity', {}).get('critical', 0)} | "
            f"High: {summary.get('severity', {}).get('high', 0)} | "
            f"Medium: {summary.get('severity', {}).get('medium', 0)} | "
            f"Low: {summary.get('severity', {}).get('low', 0)}"
        )

        if output:
            with open(output, "w") as f:
                json.dump(results, f, indent=2, default=str)
            console.print(f"\n[green]✓ Results saved to {output}[/green]")
    except Exception as e:
        handle_error("Config scan failed", e)


@scan_app.command("skills")
def scan_skills(
    path: str = typer.Option(
        ".",
        "--path", "-p",
        help="Path to skills/plugins directory"
    ),
    output: str | None = typer.Option(
        None,
        "--output", "-o",
        help="Write JSON results to file"
    ),
):
    """Scan skills/plugins for supply-chain risks."""
    console.print(Panel.fit(
        "[bold cyan]🧪 SuperClaw Supply-Chain Scan[/bold cyan]",
        border_style="cyan"
    ))
    console.print(f"  Path: [dim]{path}[/dim]")
    console.print()

    try:
        from superclaw.scanners import scan_skills as run_scan

        results = run_scan(Path(path))

        summary = results.get("summary", {})
        table = Table(title="Supply-Chain Findings", border_style="cyan")
        table.add_column("Rule", style="cyan")
        table.add_column("Severity", style="yellow")
        table.add_column("File", style="white")
        table.add_column("Line", style="white")
        table.add_column("Message", style="green")

        findings = results.get("findings", [])
        for finding in findings:
            table.add_row(
                str(finding.get("rule", "")),
                str(finding.get("severity", "")),
                str(finding.get("file", "")),
                str(finding.get("line", "")),
                str(finding.get("message", "")),
            )

        console.print(table)
        console.print(
            f"\n[bold]Total:[/bold] {summary.get('total', 0)} | "
            f"Critical: {summary.get('severity', {}).get('critical', 0)} | "
            f"High: {summary.get('severity', {}).get('high', 0)} | "
            f"Medium: {summary.get('severity', {}).get('medium', 0)} | "
            f"Low: {summary.get('severity', {}).get('low', 0)}"
        )

        if output:
            with open(output, "w") as f:
                json.dump(results, f, indent=2, default=str)
            console.print(f"\n[green]✓ Results saved to {output}[/green]")
    except Exception as e:
        handle_error("Supply-chain scan failed", e)


@app.command("behaviors")
def list_behaviors():
    """List available security behaviors."""
    try:
        from superclaw.behaviors import BEHAVIOR_REGISTRY

        table = Table(title="Available Behaviors", border_style="cyan")
        table.add_column("Name", style="cyan")
        table.add_column("Description", style="white")
        table.add_column("Severity", style="yellow")

        for name, behavior_class in BEHAVIOR_REGISTRY.items():
            behavior = behavior_class()
            desc = behavior.get_description()
            desc_display = desc[:60] + "..." if len(desc) > 60 else desc
            severity = getattr(behavior, "default_severity", None)
            severity_str = severity.value if severity else "medium"
            table.add_row(name, desc_display, severity_str)

        console.print(table)
    except Exception as e:
        handle_error("Failed to list behaviors", e)


@app.command("attacks")
def list_attacks():
    """List available attack techniques."""
    try:
        from superclaw.attacks import ATTACK_REGISTRY

        table = Table(title="Available Attack Techniques", border_style="red")
        table.add_column("Name", style="red")
        table.add_column("Description", style="white")
        table.add_column("Type", style="yellow")

        for name, attack_class in ATTACK_REGISTRY.items():
            attack = attack_class()
            desc = attack.description
            desc_display = desc[:60] + "..." if len(desc) > 60 else desc
            table.add_row(name, desc_display, attack.attack_type)

        console.print(table)
    except Exception as e:
        handle_error("Failed to list attacks", e)


@app.command("init")
def init_config(
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing config"),
):
    """Initialize SuperClaw configuration."""
    config_dir = Path.home() / ".superclaw"
    config_file = config_dir / "config.yaml"

    if config_file.exists() and not force:
        console.print(f"[yellow]Config already exists at {config_file}[/yellow]")
        console.print("Use --force to overwrite")
        return

    config_dir.mkdir(parents=True, exist_ok=True)

    default_config = """# SuperClaw Configuration

# Default target for attacks
default_target: "ws://127.0.0.1:18789"

# LLM settings for Bloom scenario generation
llm:
  provider: "anthropic"
  model: "claude-sonnet-4"

# Logging
logging:
  level: "INFO"
  file: "~/.superclaw/superclaw.log"

# Safety settings
safety:
  require_authorization: true
  local_only: true
  max_concurrent_attacks: 5
"""

    with open(config_file, "w") as f:
        f.write(default_config)

    console.print(f"[green]✓ Configuration initialized at {config_file}[/green]")


@app.command("version")
def version():
    """Show SuperClaw version."""
    from superclaw import __version__
    console.print(f"🦞 SuperClaw v{__version__}")


# ============================================================
# CODEOPTIX INTEGRATION COMMANDS
# ============================================================


@codeoptix_app.command("register")
def codeoptix_register():
    """Register SuperClaw behaviors with CodeOptiX."""
    console.print(Panel.fit(
        "[bold cyan]📦 CodeOptiX Integration[/bold cyan]",
        border_style="cyan"
    ))

    try:
        from superclaw.codeoptix import register_superclaw_behaviors

        registered = register_superclaw_behaviors()

        console.print(f"[green]✓ Registered {len(registered)} behaviors with CodeOptiX[/green]\n")

        table = Table(title="Registered Behaviors", border_style="cyan")
        table.add_column("CodeOptiX Name", style="cyan")
        table.add_column("SuperClaw Behavior", style="yellow")

        for codeoptix_name, behavior_class in registered.items():
            superclaw_name = behavior_class().name if hasattr(behavior_class, '__call__') else str(behavior_class)
            table.add_row(codeoptix_name, superclaw_name)

        console.print(table)
        console.print("\n[dim]Use these behaviors with: codeoptix eval --behaviors security-*[/dim]")

    except RuntimeError as e:
        handle_error(str(e))
    except Exception as e:
        handle_error("Failed to register behaviors", e)


@codeoptix_app.command("evaluate")
def codeoptix_evaluate(
    target: str = typer.Option(
        "ws://127.0.0.1:18789",
        "--target", "-t",
        help="Agent target URL"
    ),
    behaviors: str = typer.Option(
        "all",
        "--behaviors", "-b",
        help="Comma-separated behaviors to evaluate"
    ),
    llm_provider: str = typer.Option(
        None,
        "--llm-provider", "-l",
        help="LLM provider for multi-modal evaluation (openai, anthropic, etc.)"
    ),
    output: str | None = typer.Option(
        None,
        "--output", "-o",
        help="Output file for results"
    ),
):
    """Run CodeOptiX-style multi-modal security evaluation."""
    console.print(Panel.fit(
        "[bold cyan]🔬 CodeOptiX Security Evaluation[/bold cyan]",
        border_style="cyan"
    ))
    console.print(f"  Target: [cyan]{target}[/cyan]")
    console.print(f"  Behaviors: [yellow]{behaviors}[/yellow]")
    if llm_provider:
        console.print(f"  LLM Provider: [dim]{llm_provider}[/dim]")
    console.print()

    try:
        from superclaw.adapters import create_adapter
        from superclaw.codeoptix import create_security_engine

        # Create adapter
        adapter = create_adapter("openclaw", {"target": target})

        # Create engine
        engine = create_security_engine(
            adapter=adapter,
            llm_provider=llm_provider,
            config={"scenarios_per_behavior": 2},
        )

        # Determine behaviors
        behavior_list = None if behaviors == "all" else behaviors.split(",")

        with console.status("[cyan]Running multi-modal evaluation...[/cyan]"):
            result = engine.evaluate_security(behavior_names=behavior_list)

        # Display results
        _display_codeoptix_results(result)

        if output:
            with open(output, "w") as f:
                json.dump(result.to_dict(), f, indent=2, default=str)
            console.print(f"\n[green]✓ Results saved to {output}[/green]")

        # Exit with non-zero if failed
        if not result.overall_passed:
            raise typer.Exit(code=1)

    except ImportError as e:
        handle_error("CodeOptiX integration not available", e)
    except Exception as e:
        handle_error("Evaluation failed", e)


@codeoptix_app.command("status")
def codeoptix_status():
    """Check CodeOptiX integration status."""
    console.print("\n[bold]CodeOptiX Integration Status[/bold]\n")

    # Check CodeOptiX
    try:
        import codeoptix
        version = getattr(codeoptix, "__version__", "unknown")
        console.print(f"[green]✓ CodeOptiX installed (v{version})[/green]")

        from codeoptix.behaviors import BEHAVIOR_REGISTRY
        console.print(f"  • {len(BEHAVIOR_REGISTRY)} behaviors available")
    except ImportError:
        console.print("[yellow]✗ CodeOptiX not installed[/yellow]")
        console.print("  Install with: pip install codeoptix")

    # Check SuperClaw integration
    try:
        from superclaw.codeoptix import (
            SuperClawBehaviorAdapter,
            SecurityEvaluator,
            SecurityEvaluationEngine,
        )
        console.print("[green]✓ SuperClaw CodeOptiX integration ready[/green]")
    except ImportError as e:
        console.print(f"[red]✗ Integration module error: {e}[/red]")

    # Check LLM availability
    try:
        from codeoptix.utils.llm import LLMProvider
        console.print("[green]✓ LLM providers available[/green]")
        console.print("  Providers: openai, anthropic, google, ollama")
    except ImportError:
        console.print("[dim]• LLM providers require CodeOptiX[/dim]")

    console.print()


def _display_codeoptix_results(result):
    """Display CodeOptiX evaluation results."""
    from superclaw.codeoptix.engine import SecurityEngineResult

    # Overall status
    status_color = "green" if result.overall_passed else "red"
    status_text = "PASSED" if result.overall_passed else "FAILED"

    console.print(Panel(
        f"[bold {status_color}]Security Evaluation: {status_text}[/bold {status_color}]\n\n"
        f"Overall Score: {result.overall_score:.1%}\n"
        f"Scenarios Tested: {result.scenarios_tested}\n"
        f"Scenarios Passed: {result.scenarios_passed}",
        title="Results",
        border_style=status_color,
    ))

    # Behavior details
    if result.behaviors:
        table = Table(title="Behavior Results", border_style="cyan")
        table.add_column("Behavior", style="cyan")
        table.add_column("Status")
        table.add_column("Score", style="yellow")
        table.add_column("Severity")
        table.add_column("Static Analysis")

        severity_colors = {
            "critical": "bold red",
            "high": "red",
            "medium": "yellow",
            "low": "green",
        }

        for name, behavior_result in result.behaviors.items():
            status = "[green]PASS[/green]" if behavior_result.passed else "[red]FAIL[/red]"
            score = f"{behavior_result.score:.1%}"
            sev_color = severity_colors.get(behavior_result.severity, "white")
            severity = f"[{sev_color}]{behavior_result.severity}[/{sev_color}]"

            static = behavior_result.static_analysis
            static_info = f"{static.get('issue_count', 0)} issues" if static.get('status') == 'completed' else static.get('status', '-')

            table.add_row(name, status, score, severity, static_info)

        console.print(table)

    # Summary
    if result.summary:
        console.print("\n[bold]Summary:[/bold]")
        summary = result.summary
        console.print(f"  Total: {summary.get('total_behaviors', 0)} behaviors")
        console.print(f"  [green]Passed: {summary.get('passed', 0)}[/green]")
        console.print(f"  [red]Failed: {summary.get('failed', 0)}[/red]")
        if summary.get('critical', 0) > 0:
            console.print(f"  [bold red]Critical: {summary.get('critical', 0)}[/bold red]")


# ============================================================
# HELPER FUNCTIONS
# ============================================================


def _display_attack_results(results: dict):
    """Display attack results in a table."""
    table = Table(title="Attack Results", border_style="red")
    table.add_column("Behavior", style="cyan")
    table.add_column("Status", style="white")
    table.add_column("Score", style="yellow")
    table.add_column("Findings", style="red")

    for behavior_name, behavior_result in results.get("behaviors", {}).items():
        status = "[green]PASSED[/green]" if behavior_result.get("passed") else "[red]FAILED[/red]"
        score = f"{behavior_result.get('score', 0):.2f}"
        findings = len(behavior_result.get("evidence", []))
        table.add_row(behavior_name, status, score, str(findings))

    console.print(table)

    overall = results.get("overall_score", 0)
    color = "green" if overall > 0.8 else "yellow" if overall > 0.5 else "red"
    console.print(f"\nOverall Security Score: [{color}]{overall:.2f}[/{color}]")


def _display_evaluation_results(results: dict):
    """Display evaluation results."""
    _display_attack_results(results)


def _display_audit_summary(results: dict):
    """Display audit summary."""
    summary = results.get("summary", {})

    console.print("\n[bold]Audit Summary[/bold]")
    console.print(f"  Total Behaviors Tested: {summary.get('total_behaviors', 0)}")
    console.print(f"  Passed: [green]{summary.get('passed', 0)}[/green]")
    console.print(f"  Failed: [red]{summary.get('failed', 0)}[/red]")
    console.print(f"  Critical Findings: [red]{summary.get('critical', 0)}[/red]")
    console.print(f"  High Findings: [yellow]{summary.get('high', 0)}[/yellow]")
    console.print(f"  Medium Findings: [blue]{summary.get('medium', 0)}[/blue]")
    console.print(f"  Low Findings: [dim]{summary.get('low', 0)}[/dim]")


def main():
    """Entry point for SuperClaw CLI."""
    app()


if __name__ == "__main__":
    main()
