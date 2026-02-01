# Quick Start

## 1. List Available Behaviors

```bash
superclaw behaviors
```

## 2. List Attack Techniques

```bash
superclaw attacks
```

## 3. Run a Quick Security Scan

```bash
# Attack a local OpenClaw instance
superclaw attack openclaw --target ws://127.0.0.1:18789 --behaviors all
```

## 4. Generate Attack Scenarios

```bash
superclaw generate scenarios --behavior prompt_injection --num-scenarios 10
```

## 5. Run Full Security Audit

```bash
superclaw audit openclaw --comprehensive --report-format html --output audit-report
```

## 6. View Results

Open `audit-report.html` in your browser to see the full security report.

## 7. Scan Configuration (Optional)

```bash
superclaw scan config
```

## Python API

```python
from superclaw.attacks import run_attack
from superclaw.behaviors import BEHAVIOR_REGISTRY

# Run attack
results = run_attack(
    agent_type="openclaw",
    target="ws://127.0.0.1:18789",
    behaviors=["prompt-injection-resistance"],
)

print(f"Score: {results['overall_score']:.1%}")
```
