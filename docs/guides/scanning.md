# Scanning & Drift

## Configuration Scanning

Scan your SuperClaw config for risky settings:

```bash
superclaw scan config
superclaw scan config --output scan.json
```

What it checks:
- Public targets or insecure `ws://` usage
- Missing auth/authorization settings
- Weak logging configuration
- Missing LLM provider/model

## Supply-Chain Scanning

Scan skills/plugins for risky patterns:

```bash
superclaw scan skills --path /path/to/skills
```

What it checks:
- Suspicious `package.json` install scripts
- Unsafe exec/eval usage in JS/TS/Python/Shell

## Drift Comparison

Compare two runs to detect regressions:

```bash
superclaw report drift --baseline baseline.json --current current.json
```

The drift report flags:
- Behavior regressions (failures or score drops)
- Scenario regressions (per-scenario pass/fail changes)
