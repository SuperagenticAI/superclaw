# Running Attacks

## Basic Attack

```bash
superclaw attack openclaw --target ws://127.0.0.1:18789
```

## Specify Behaviors

```bash
superclaw attack openclaw \
  --behaviors prompt-injection-resistance,tool-policy-enforcement
```

## Specify Techniques

```bash
superclaw attack openclaw \
  --techniques prompt-injection,encoding,jailbreak
```

## Dry Run

```bash
superclaw attack openclaw --dry-run
```

## Save Results

```bash
superclaw attack openclaw --output results.json
```

## Mock/Offline Testing

```bash
# Run attacks without a live agent
superclaw attack mock --behaviors prompt-injection-resistance

# Evaluate a mock agent with scenarios
superclaw evaluate mock --scenarios scenarios.json
```

## Drift Comparison

```bash
# Compare two runs and flag regressions
superclaw report drift --baseline baseline.json --current current.json
```

## Evidence Ledger

Results include a normalized evidence ledger per attack/scenario:

```json
{
  "messages": [],
  "tool_calls": [],
  "tool_results": [],
  "artifacts": [],
  "secrets_detected": []
}
```

## Python API

```python
from superclaw.attacks import run_attack

results = run_attack(
    agent_type="openclaw",
    target="ws://127.0.0.1:18789",
    behaviors=["prompt-injection-resistance"],
    techniques=["prompt-injection", "encoding"],
)

for behavior, data in results["behaviors"].items():
    print(f"{behavior}: {'PASS' if data['passed'] else 'FAIL'}")
```

## Attack ACP Agents

```bash
superclaw attack acp --command "opencode acp" --project /path/to/project
```
