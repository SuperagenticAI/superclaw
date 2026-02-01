# 🦞 SuperClaw

**SuperClaw — Red-Team AI Agents Before They Red-Team You**  
Scenario-driven, behavior-first security testing for autonomous agents.

---

## What is SuperClaw?

SuperClaw is a comprehensive security testing framework for AI coding agents. It systematically identifies vulnerabilities through:

- **Prompt Injection** - Direct and indirect injection attacks
- **Tool Policy Bypass** - Alias confusion, group expansion exploits  
- **Sandbox Escape** - Container boundary testing
- **Multi-Agent Trust** - Inter-agent exploitation

## Key Features

| Feature | Description |
|---------|-------------|
| 🎯 **Attack Library** | 5 attack techniques with 100+ payloads |
| 🔍 **Behavior Specs** | 6 security behaviors with severity levels |
| 🌸 **Bloom Integration** | LLM-powered scenario generation |
| 📊 **Multi-Format Reports** | HTML, JSON, SARIF for CI/CD |
| 🔬 **CodeOptiX Integration** | Multi-modal evaluation pipeline |

## Quick Start

```bash
# Install
pip install superclaw

# Or with uv
uv pip install superclaw

# Run a security scan
superclaw attack openclaw --target ws://127.0.0.1:18789

# Generate report
superclaw audit openclaw --comprehensive --report-format html
```

## Part of Superagentic AI Ecosystem

```
┌─────────────────────────────────────────────────────────────┐
│                  Superagentic AI Ecosystem                  │
├─────────────────────────────────────────────────────────────┤
│  SuperQode    │  TUI interface for SuperQE, CI/automation  │
│  SuperQE      │  Quality Engineering core engine            │
│  SuperClaw    │  Agent security testing framework ◄── YOU   │
│  CodeOptiX    │  Code optimization & evaluation engine      │
│  Bloom        │  Behavioral evaluation scenario generation  │
└─────────────────────────────────────────────────────────────┘
```

## Installation Options

=== "pip"

    ```bash
    pip install superclaw
    ```

=== "uv"

    ```bash
    uv pip install superclaw
    ```

=== "With CodeOptiX"

    ```bash
    pip install superclaw[codeoptix]
    ```

=== "From SuperQode"

    ```bash
    pip install superqode[security]
    ```

## Next Steps

## ⚠️ Security and Ethical Use

SuperClaw is **for authorized security testing only**. You must:
- Obtain explicit permission before testing real systems
- Run tests in sandboxed or isolated environments
- Treat automated findings as signals, not proof

- [Installation Guide](getting-started/installation.md)
- [Quick Start Tutorial](getting-started/quickstart.md)
- [Architecture Overview](architecture/overview.md)
