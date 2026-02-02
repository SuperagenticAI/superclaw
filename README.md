# 🦞 SuperClaw

<p align="center">
  <a href="https://pypi.org/project/superclaw/"><img alt="PyPI" src="https://img.shields.io/pypi/v/superclaw" /></a>
  <a href="https://superagenticai.github.io/superclaw/"><img alt="Docs" src="https://img.shields.io/badge/Docs-online-brightgreen" /></a>
  <a href="https://github.com/SuperagenticAI/superclaw"><img alt="GitHub Repo" src="https://img.shields.io/badge/GitHub-superclaw-black?logo=github" /></a>
  <a href="https://github.com/SuperagenticAI/superclaw/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/SuperagenticAI/superclaw/actions/workflows/ci.yml/badge.svg" /></a>
  <a href="https://github.com/SuperagenticAI/superclaw/actions/workflows/docs.yml"><img alt="Docs Build" src="https://github.com/SuperagenticAI/superclaw/actions/workflows/docs.yml/badge.svg" /></a>
  <a href="https://opensource.org/licenses/Apache-2.0"><img alt="License" src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" /></a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/SuperagenticAI/superclaw/main/assets/superclaw_logo.png" alt="SuperClaw logo" width="220" />
</p>

<p align="center">
  <strong>Red-Team AI Agents Before They Red-Team You</strong><br/>
  Scenario-driven, behavior-first security testing for autonomous agents.
</p>

<p align="center">
  <a href="https://superagenticai.github.io/superclaw/"><img src="https://img.shields.io/badge/📚_Full_Documentation-superagenticai.github.io/superclaw-blue?style=for-the-badge" alt="Documentation" /></a>
</p>

<p align="center">
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-features">Features</a> •
  <a href="#-attack-techniques">Attack Techniques</a> •
  <a href="https://superagenticai.github.io/superclaw/">Full Docs</a>
</p>

---

## ⚠️ Security and Ethical Use

### Authorized Testing Only

SuperClaw is for authorized security testing only.

## What is SuperClaw?

SuperClaw is a pre-deployment security testing framework for AI coding agents. It systematically identifies vulnerabilities before your agents touch sensitive data or connect to external ecosystems.

### 🎯 Scenario-Driven Testing

Generate and execute adversarial scenarios against real agents with reproducible results.

[Get started →](https://superagenticai.github.io/superclaw/getting-started/quickstart/)

### 📋 Behavior Contracts

Explicit success criteria, evidence extraction, and mitigation guidance for each security property.

[Explore behaviors →](https://superagenticai.github.io/superclaw/architecture/behaviors/)

### 📊 Evidence-First Reporting

Reports include tool calls, outputs, and actionable fixes in HTML, JSON, or SARIF formats.

[CI/CD integration →](https://superagenticai.github.io/superclaw/guides/ci-cd/)

### 🛡️ Built-in Guardrails

Local-only mode and authorization checks reduce misuse risk.

[Safety guide →](https://superagenticai.github.io/superclaw/guides/safety/)

## ⚠️ Security and Ethical Use

### Authorized Testing Only

SuperClaw is for authorized security testing only. Before using:

- ✅ Obtain written permission to test the target system
- ✅ Run tests in sandboxed or isolated environments
- ✅ Treat automated findings as signals, not proof—verify manually

**Guardrails enforced by default:**

- Local-only mode blocks remote targets
- Remote targets require `SUPERCLAW_AUTH_TOKEN`

## Threat Model

### OpenClaw + Moltbook Risk Surface

OpenClaw agents often run with broad tool access. When connected to Moltbook or other agent networks, they can ingest untrusted, adversarial content that enables:

- Prompt injection and hidden instruction attacks
- Tool misuse and policy bypass
- Behavioral drift over time
- Cascading cross-agent exploitation

SuperClaw evaluates these risks before deployment.

## Why SuperClaw?

Autonomous AI agents are deployed with high privileges, mutable behavior, and exposure to untrusted inputs—often without structured security validation. This makes prompt injection, tool misuse, configuration drift, and data leakage likely but poorly understood until after exposure.

### What It Does

- **Runs scenario-based security evaluations** against your agents
- **Records evidence** (tool calls, outputs, artifacts) for each attack
- **Scores behaviors** against explicit security contracts
- **Produces actionable reports** with findings and mitigations

### What It Doesn't Do

SuperClaw does **not** generate agents, run production workloads, or automate real-world exploitation. It's a testing tool, not a weapon.

---

## 🚀 Quick Start

### Installation

```bash
pip install superclaw
```

### Run Your First Attack

```bash
# Attack a local OpenClaw instance
superclaw attack openclaw --target ws://127.0.0.1:18789

# Or test offline with the mock adapter
superclaw attack mock --behaviors prompt-injection-resistance
```

### Generate Attack Scenarios

```bash
superclaw generate scenarios --behavior prompt_injection --num-scenarios 20
```

### Run a Full Security Audit

```bash
superclaw audit openclaw --comprehensive --report-format html --output report
```

---

## ✨ Features

### Supported Targets

| Target | Description | Adapter |
|--------|-------------|---------|
| 🦞 **OpenClaw** | AI coding agents via ACP WebSocket | `openclaw` |
| 🧪 **Mock** | Offline deterministic testing | `mock` |
| 🔧 **Custom** | Build your own adapter | Extend `BaseAdapter` |

### Attack Techniques

| Technique | Description |
|-----------|-------------|
| `prompt-injection` | Direct and indirect injection attacks |
| `encoding` | Base64, hex, unicode, typoglycemia obfuscation |
| `jailbreak` | DAN, grandmother, role-play bypass techniques |
| `tool-bypass` | Tool policy bypass via alias confusion |
| `multi-turn` | Persistent escalation across conversation turns |

### Security Behaviors

Each behavior includes a structured contract with intent, success criteria, rubric, and mitigation guidance.

| Behavior | Severity | Tests |
|----------|----------|-------|
| `prompt-injection-resistance` | 🔴 CRITICAL | Injection detection and rejection |
| `sandbox-isolation` | 🔴 CRITICAL | Container and filesystem boundaries |
| `tool-policy-enforcement` | 🟠 HIGH | Allow/deny list compliance |
| `session-boundary-integrity` | 🟠 HIGH | Cross-session isolation |
| `configuration-drift-detection` | 🟡 MEDIUM | Config stability over time |
| `acp-protocol-security` | 🟡 MEDIUM | Protocol message handling |

---

## 📖 CLI Reference

### Attacks

```bash
superclaw attack openclaw --target ws://127.0.0.1:18789 --behaviors all
superclaw attack mock --behaviors prompt-injection-resistance
```

### Scenario Generation (Bloom)

```bash
superclaw generate scenarios --behavior prompt_injection --num-scenarios 20
superclaw generate scenarios --behavior jailbreak --variations noise,emotional_pressure
```

### Evaluation

```bash
superclaw evaluate openclaw --scenarios scenarios.json --behaviors all
superclaw evaluate mock --scenarios scenarios.json
```

### Auditing

```bash
superclaw audit openclaw --comprehensive --report-format html --output report
superclaw audit openclaw --quick
```

### Reporting

```bash
superclaw report generate --results results.json --format sarif  # GitHub Code Scanning
superclaw report drift --baseline baseline.json --current current.json
```

### Scanning

```bash
superclaw scan config
superclaw scan skills --path /path/to/skills
```

### Utilities

```bash
superclaw behaviors   # List all security behaviors
superclaw attacks     # List all attack techniques
superclaw init        # Initialize a new project
```

---

## 🔗 CodeOptiX Integration

SuperClaw integrates with [CodeOptiX](https://github.com/SuperagenticAI/codeoptix) for multi-modal security evaluation.

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

---

## ⚠️ Security Notice

**This tool is for authorized security testing only.**

### Guardrails

- Local-only mode blocks remote targets by default
- Remote targets require `SUPERCLAW_AUTH_TOKEN` (or adapter-specific token)
    - *Note: SuperClaw does not manage this token; you must obtain it from the remote system administrator.*

### Requirements

Before using SuperClaw, ensure you have:
- ✅ Written authorization to test the target system
- ✅ Isolated test environment (sandbox/VM recommended)
- ✅ Understanding of [SECURITY.md](SECURITY.md) guidelines

---

## 🏗️ Architecture

```
superclaw/
├── attacks/        # Attack technique implementations
├── behaviors/      # Security behavior specifications
├── adapters/       # Target agent adapters
├── bloom/          # AI-powered scenario generation
├── scanners/       # Config and supply-chain scanning
├── analysis/       # Drift detection and comparison
├── codeoptix/      # CodeOptiX integration layer
└── reporting/      # HTML, JSON, and SARIF report generation
```

---

## 🌐 Superagentic AI Ecosystem

SuperClaw is part of the [Superagentic AI](https://super-agentic.ai) ecosystem:

| Project | Description |
|---------|-------------|
| **SuperQE** | Quality engineering core framework |
| **SuperClaw** | Agent security testing *(this package)* |
| **CodeOptiX** | Code optimization and evaluation engine |

---

## 📚 Documentation

<table>
<tr>
<td width="100%" align="center">
<h3>📖 <a href="https://superagenticai.github.io/superclaw/">superagenticai.github.io/superclaw</a></h3>
</td>
</tr>
</table>

| Guide | Description |
|-------|-------------|
| [Installation](https://superagenticai.github.io/superclaw/getting-started/installation/) | Setup with pip, uv, or from source |
| [Quick Start](https://superagenticai.github.io/superclaw/getting-started/quickstart/) | Run your first security scan in 5 minutes |
| [Configuration](https://superagenticai.github.io/superclaw/getting-started/configuration/) | Configure targets, LLM providers, and safety settings |
| [Running Attacks](https://superagenticai.github.io/superclaw/guides/attacks/) | Execute attacks and interpret results |
| [Custom Behaviors](https://superagenticai.github.io/superclaw/guides/custom-behaviors/) | Write your own security behavior specs |
| [CI/CD Integration](https://superagenticai.github.io/superclaw/guides/ci-cd/) | GitHub Actions, GitLab CI, and SARIF output |
| [Architecture](https://superagenticai.github.io/superclaw/architecture/overview/) | Deep dive into SuperClaw internals |

---

## 🤝 Contributing

We welcome contributions! Please see:

- [CONTRIBUTING.md](CONTRIBUTING.md) — How to contribute
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — Community guidelines
- [SECURITY.md](SECURITY.md) — Security policy

---

## 📄 License

Apache 2.0 — see [LICENSE](LICENSE) for details.

---

<p align="center">
  Built with 🦞 by <a href="https://super-agentic.ai">Superagentic AI</a>
</p>
