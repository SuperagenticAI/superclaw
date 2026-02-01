# SuperQode Integration

SuperClaw integrates seamlessly with SuperQode for security scanning.

## Installation

```bash
# Install SuperQode with security support
pip install superqode[security]
```

## CLI Commands

```bash
# Check SuperClaw status
superqode security status

# List behaviors
superqode security behaviors

# List attacks
superqode security attacks

# Quick scan
superqode security quick --agent openclaw

# Full scan
superqode security scan --agent openclaw --mode comprehensive

# Security audit with report
superqode security audit --format html --output report.html
```

## Python API

```python
from superqode.integrations import (
    run_security_scan,
    run_quick_scan,
    run_comprehensive_scan,
)

# Quick scan
result = run_quick_scan(agent_type="openclaw")
print(f"Passed: {result.passed}")

# Full scan
result = run_comprehensive_scan(
    agent_type="openclaw",
    target="ws://127.0.0.1:18789",
)

for behavior, data in result.behaviors.items():
    print(f"{behavior}: {data['score']:.1%}")
```

## Combined Workflow

```bash
# Run QE session
superqode qe run .

# Run security scan
superqode security audit --comprehensive

# View suggestions
superqode suggestions list
```

## Configuration

Add to your `superqode.yaml`:

```yaml
security:
  enabled: true
  agent: openclaw
  target: ws://127.0.0.1:18789
  behaviors:
    - prompt-injection-resistance
    - tool-policy-enforcement
    - sandbox-isolation
```
