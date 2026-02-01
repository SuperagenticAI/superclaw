# Quick Start

Get up and running with SuperClaw in under 5 minutes.

---

## Prerequisites

- Python 3.12+
- A target agent to test (or use the mock adapter for offline testing)

---

## Step 1: Install SuperClaw

```bash
pip install superclaw
```

Verify the installation:

```bash
superclaw --version
```

---

## Step 2: Explore Available Options

### List Security Behaviors

```bash
superclaw behaviors
```

This shows all security properties SuperClaw can test:

| Behavior | Severity | Description |
|----------|----------|-------------|
| `prompt-injection-resistance` | CRITICAL | Detects injection attempts |
| `sandbox-isolation` | CRITICAL | Tests container boundaries |
| `tool-policy-enforcement` | HIGH | Validates allow/deny lists |
| `session-boundary-integrity` | HIGH | Verifies session isolation |
| `configuration-drift-detection` | MEDIUM | Detects config changes |
| `acp-protocol-security` | MEDIUM | Validates protocol handling |

### List Attack Techniques

```bash
superclaw attacks
```

---

## Step 3: Run Your First Attack

### Option A: Test a Live OpenClaw Agent

If you have an OpenClaw agent running locally:

```bash
superclaw attack openclaw --target ws://127.0.0.1:18789 --behaviors all
```

### Option B: Offline Testing with Mock Adapter

No live agent? Use the mock adapter for deterministic testing:

```bash
superclaw attack mock --behaviors prompt-injection-resistance
```

---

## Step 4: Generate Attack Scenarios

Use Bloom to generate LLM-powered attack scenarios:

```bash
# Generate 10 prompt injection scenarios
superclaw generate scenarios --behavior prompt_injection --num-scenarios 10

# Generate jailbreak scenarios with variations
superclaw generate scenarios --behavior jailbreak --variations noise,emotional_pressure
```

!!! note "LLM Configuration Required"
    Scenario generation requires an LLM provider. Set your API key:
    ```bash
    export OPENAI_API_KEY="sk-..."
    # or
    export ANTHROPIC_API_KEY="sk-ant-..."
    ```

---

## Step 5: Run a Comprehensive Audit

Generate a full security report:

```bash
superclaw audit openclaw \
  --target ws://127.0.0.1:18789 \
  --comprehensive \
  --report-format html \
  --output audit-report
```

Open `audit-report.html` in your browser to view the full security assessment.

---

## Step 6: Review Results

### Understanding the Output

Each attack produces results including:

- **Behavior scores** (0.0 - 1.0, higher is more secure)
- **Pass/Fail status** for each security property
- **Evidence** (tool calls, responses, artifacts)
- **Severity** ratings for failures

### Example Output

```
┌─────────────────────────────────────────────────────────────┐
│                    Security Assessment                       │
├─────────────────────────────────────────────────────────────┤
│ Target: ws://127.0.0.1:18789                                │
│ Behaviors tested: 6                                          │
│ Overall score: 78.3%                                         │
├─────────────────────────────────────────────────────────────┤
│ prompt-injection-resistance    │ ✓ PASS │ 0.85 │ CRITICAL   │
│ sandbox-isolation              │ ✓ PASS │ 1.00 │ CRITICAL   │
│ tool-policy-enforcement        │ ✗ FAIL │ 0.45 │ HIGH       │
│ session-boundary-integrity     │ ✓ PASS │ 0.90 │ HIGH       │
│ configuration-drift-detection  │ ✓ PASS │ 1.00 │ MEDIUM     │
│ acp-protocol-security          │ ✗ FAIL │ 0.50 │ MEDIUM     │
└─────────────────────────────────────────────────────────────┘
```

---

## Step 7: Optional Configuration

### Initialize Configuration File

```bash
superclaw init
```

Creates `~/.superclaw/config.yaml` with default settings.

### Scan Your Configuration

Check for security issues in your config:

```bash
superclaw scan config
```

---

## Python API

Use SuperClaw programmatically:

```python
from superclaw.attacks import run_attack
from superclaw.behaviors import BEHAVIOR_REGISTRY

# Run attack
results = run_attack(
    agent_type="openclaw",
    target="ws://127.0.0.1:18789",
    behaviors=["prompt-injection-resistance"],
)

print(f"Overall Score: {results['overall_score']:.1%}")

for behavior, data in results["behaviors"].items():
    status = "✓ PASS" if data["passed"] else "✗ FAIL"
    print(f"{behavior}: {status} ({data['score']:.2f})")
```

---

## Next Steps

- [Configuration Guide](configuration.md) — Customize targets, LLM providers, and safety settings
- [Running Attacks](../guides/attacks.md) — Deep dive into attack options
- [Custom Behaviors](../guides/custom-behaviors.md) — Write your own security tests
- [CI/CD Integration](../guides/ci-cd.md) — Automate security scanning in your pipeline
