# Installation

Get SuperClaw installed and ready to use.

---

## Requirements

| Requirement | Version |
|-------------|---------|
| Python | 3.12+ |
| Package Manager | pip or uv |

---

## Installation Methods

### Using pip

```bash
pip install superclaw
```

### Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package manager:

```bash
uv pip install superclaw
```

### From Source

Clone the repository and install in development mode:

```bash
git clone https://github.com/SuperagenticAI/superclaw.git
cd superclaw
uv sync
```

---

## Optional Dependencies

SuperClaw supports optional features through extras:

=== "CodeOptiX Integration"

    Multi-modal security evaluation with CodeOptiX:
    
    ```bash
    pip install superclaw[codeoptix]
    ```

=== "Development Tools"

    For contributing to SuperClaw:
    
    ```bash
    pip install superclaw[dev]
    ```

=== "Documentation"

    For building the documentation locally:
    
    ```bash
    pip install superclaw[docs]
    ```

=== "Everything"

    Install all optional dependencies:
    
    ```bash
    pip install superclaw[all]
    ```

---

## Verify Installation

Check that SuperClaw is installed correctly:

```bash
# Show version
superclaw --version

# List available behaviors
superclaw behaviors

# List attack techniques
superclaw attacks

# Show help
superclaw --help
```

Expected output:

```
SuperClaw v0.1.1 - Agent Security Testing Framework

Available behaviors:
  prompt-injection-resistance    [CRITICAL] Tests injection detection
  tool-policy-enforcement        [HIGH]     Tests allow/deny lists
  sandbox-isolation              [CRITICAL] Tests container boundaries
  session-boundary-integrity     [HIGH]     Tests session isolation
  configuration-drift-detection  [MEDIUM]   Tests config stability
  acp-protocol-security          [MEDIUM]   Tests protocol handling
```

---

## Development Setup

For contributors working on SuperClaw:

### Clone and Install

```bash
git clone https://github.com/SuperagenticAI/superclaw.git
cd superclaw
uv sync
```

### Common Development Commands

```bash
# Sync dependencies
uv sync

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=superclaw

# Type checking
uv run mypy src/superclaw

# Linting
uv run ruff check src/

# Format code
uv run ruff format src/

# Run CLI
uv run superclaw --help

# Build package
uv build

# Serve documentation locally
uv run mkdocs serve
```

### Pre-commit Hooks

Install pre-commit hooks to ensure code quality:

```bash
pip install pre-commit
pre-commit install
```

---

## Troubleshooting

### Python Version Error

If you see a Python version error:

```
ERROR: Package requires Python >=3.12
```

Ensure you're using Python 3.12 or later:

```bash
python --version
# or
python3 --version
```

### Import Errors

If you see import errors after installation, try reinstalling:

```bash
pip uninstall superclaw
pip install superclaw
```

### WebSocket Connection Issues

If attacks fail with connection errors:

1. Verify the target is running and accessible
2. Check the target URL format: `ws://host:port`
3. Ensure firewalls allow the connection

---

## Next Steps

- [Quick Start](quickstart.md) — Run your first security scan
- [Configuration](configuration.md) — Customize settings
