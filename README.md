<p align="center">
  <a href="https://pypi.org/project/superclaw/"><img alt="PyPI" src="https://badge.fury.io/py/superclaw.svg" /></a>
  <a href="https://github.com/SuperagenticAI/superclaw"><img alt="GitHub Repo" src="https://img.shields.io/badge/GitHub-superclaw-black?logo=github" /></a>
  <a href="https://github.com/SuperagenticAI/superclaw/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/SuperagenticAI/superclaw/actions/workflows/ci.yml/badge.svg" /></a>
  <a href="https://github.com/SuperagenticAI/superclaw/actions/workflows/docs.yml"><img alt="Docs" src="https://github.com/SuperagenticAI/superclaw/actions/workflows/docs.yml/badge.svg" /></a>
  <a href="https://opensource.org/licenses/Apache-2.0"><img alt="License" src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" /></a>
</p>

# 🦞 SuperClaw

<p align="center">
  <img src="assets/superclaw_logo.png" alt="SuperClaw logo" width="220" />
</p>

<p align="center">
  <strong>SuperClaw — Red-Team AI Agents Before They Red-Team You</strong><br/>
  Scenario-driven, behavior-first security testing for autonomous agents.
</p>

SuperClaw is a security testing framework for AI coding agents such as **OpenClaw** and agent ecosystems like **Moltbook**. It identifies vulnerabilities through prompt injection, tool policy bypass, sandbox escape, and multi-agent trust exploitation.

## OpenClaw + Moltbook Threat Model

> **Threat Model**  
> OpenClaw agents often run with broad tool access. When connected to **Moltbook** or other agent networks, they can ingest untrusted, adversarial content that enables:
> - Prompt injection and hidden instruction attacks  
> - Tool misuse and policy bypass  
> - Behavioral drift over time  
> - Cascading cross‑agent exploitation  
> SuperClaw is built to evaluate these risks **before** deployment.

## Problem & Solution (Summary)

**Problem:** Autonomous agents are being deployed with high privilege, mutable behavior, and exposure to untrusted inputs—without structured security validation. This makes prompt injection, tool misuse, configuration drift, and data leakage likely, but poorly understood until after exposure.

**Solution:** SuperClaw is a **pre‑deployment, behavior‑driven red‑teaming framework** that stress‑tests existing agents. It runs scenario‑based evaluations, records evidence (tool calls, outputs, artifacts), scores behaviors against explicit contracts, and produces actionable reports before agents touch sensitive data or external ecosystems.

**Non‑goals:** SuperClaw does **not** generate agents, run production workloads, or automate real‑world exploitation.

## ⚠️ Security Notice

**This tool is for authorized security testing only.** See [SECURITY.md](SECURITY.md) for:
- Authorization requirements
- Containment requirements (sandbox/VM)
- False positive handling
- Data safety guidelines

Guardrails:
- Local-only mode blocks remote targets by default
- Remote targets require `SUPERCLAW_AUTH_TOKEN` (or adapter token)

## Supported Targets

- 🦞 **OpenClaw** — ACP WebSocket adapter
- 🧪 **Mock** — Offline deterministic testing
- 🔧 **Custom** — Extend via adapters

## Quick Start

```bash
# Install
pip install superclaw

# Attack OpenClaw (local instance)
superclaw attack openclaw --target ws://127.0.0.1:18789

# Generate attack scenarios
superclaw generate scenarios --behavior prompt_injection --num-scenarios 20

# Run security audit
superclaw audit openclaw --comprehensive --report-format html --output report

# Offline testing
superclaw attack mock --behaviors prompt-injection-resistance
```

## Attack Techniques

| Technique | Description |
|-----------|-------------|
| `prompt-injection` | Direct/indirect injection attacks |
| `encoding` | Base64, hex, unicode, typoglycemia obfuscation |
| `jailbreak` | DAN, grandmother, role-play techniques |
| `tool-bypass` | Tool policy bypass via alias confusion |
| `multi-turn` | Multi-turn persistent escalation attacks |

## Security Behaviors

Each behavior ships with a structured contract (intent, success criteria, rubric, mitigation).

| Behavior | Severity | Description |
|----------|----------|-------------|
| `prompt-injection-resistance` | CRITICAL | Tests injection detection |
| `tool-policy-enforcement` | HIGH | Tests allow/deny lists |
| `sandbox-isolation` | CRITICAL | Tests container boundaries |
| `session-boundary-integrity` | HIGH | Tests session isolation |
| `configuration-drift-detection` | MEDIUM | Tests config stability |
| `acp-protocol-security` | MEDIUM | Tests protocol handling |

## CLI Commands

```bash
# Attacks
superclaw attack openclaw --target ws://127.0.0.1:18789 --behaviors all
superclaw attack mock --behaviors prompt-injection-resistance

# Scenario generation (Bloom)
superclaw generate scenarios --behavior prompt_injection --num-scenarios 20
superclaw generate scenarios --behavior jailbreak --variations noise,emotional_pressure

# Evaluation
superclaw evaluate openclaw --scenarios scenarios.json --behaviors all
superclaw evaluate mock --scenarios scenarios.json

# Audit
superclaw audit openclaw --comprehensive --report-format html --output report
superclaw audit openclaw --quick

# Reporting
superclaw report generate --results results.json --format sarif  # For GitHub Code Scanning
superclaw report drift --baseline baseline.json --current current.json

# Scanning
superclaw scan config
superclaw scan skills --path /path/to/skills

# Utilities
superclaw behaviors
superclaw attacks
superclaw init
```

## CodeOptiX Integration

SuperClaw integrates with [CodeOptiX](https://github.com/SuperagenticAI/codeoptix) for multi-modal evaluation:

```bash
# Install with CodeOptiX support
pip install superclaw[codeoptix]

# Check integration status
superclaw codeoptix status

# Register behaviors with CodeOptiX
superclaw codeoptix register

# Run multi-modal evaluation
superclaw codeoptix evaluate --target ws://127.0.0.1:18789 --llm-provider openai
```

### Python API

```python
from superclaw.codeoptix import SecurityEvaluationEngine
from superclaw.adapters import create_adapter

adapter = create_adapter("openclaw", {"target": "ws://127.0.0.1:18789"})
engine = SecurityEvaluationEngine(adapter)

result = engine.evaluate_security(behavior_names=["prompt-injection-resistance"])
print(f"Score: {result.overall_score:.1%}")
print(f"Passed: {result.overall_passed}")
```

## Architecture

```
superclaw/
├── attacks/          # Attack implementations
│   ├── prompt_injection.py
│   ├── encoding.py
│   ├── jailbreaks.py
│   ├── tool_bypass.py
│   └── multi_turn.py
├── behaviors/        # Security behavior specs
│   ├── injection_resistance.py
│   ├── tool_policy.py
│   ├── sandbox_isolation.py
│   ├── session_boundary.py
│   ├── config_drift.py
│   └── protocol_security.py
├── adapters/         # Agent adapters
│   ├── openclaw.py
│   ├── mock.py
│   └── base.py
├── bloom/            # Scenario generation
│   ├── ideation.py
│   ├── rollout.py
│   └── judgment.py
├── scanners/         # Config + supply-chain scanning
├── analysis/         # Drift comparison
├── codeoptix/        # CodeOptiX integration
│   ├── adapter.py    # Behavior adapter
│   ├── evaluator.py  # Security evaluator
│   └── engine.py     # Evaluation engine
└── reporting/        # Report generation
    ├── html.py
    ├── json_report.py
    └── sarif.py
```

## Part of Superagentic AI Ecosystem

- **SuperQE** - Quality Engineering core
- **SuperClaw** - Agent security testing (this package)
- **CodeOptiX** - Code optimization engine

## Open Source

- [LICENSE](LICENSE)
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [SECURITY.md](SECURITY.md)

Built by [Superagentic AI](https://super-agentic.ai) · GitHub: [SuperagenticAI/superclaw](https://github.com/SuperagenticAI/superclaw)

## License

Apache 2.0
