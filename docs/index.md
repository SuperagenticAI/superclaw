# 🦞 SuperClaw

**SuperClaw: Red-Team AI Agents Before They Red-Team You**  
Scenario-driven, behavior-first security testing for autonomous agents.

---

## ⚠️ Security and Ethical Use (Read First)

SuperClaw is **for authorized security testing only**. You must:
- Obtain explicit permission before testing real systems
- Run tests in sandboxed or isolated environments
- Treat automated findings as signals, not proof

Guardrails:
- Local-only mode blocks remote targets by default
- Remote targets require `SUPERCLAW_AUTH_TOKEN` (or adapter token)

## What is SuperClaw?

SuperClaw is a comprehensive security testing framework for AI coding agents such as **OpenClaw** and agent ecosystems like **Moltbook**. It systematically identifies vulnerabilities through:

- **Prompt Injection** - Direct and indirect injection attacks
- **Tool Policy Bypass** - Alias confusion, group expansion exploits  
- **Sandbox Escape** - Container boundary testing
- **Multi-Agent Trust** - Inter-agent exploitation

## OpenClaw + Moltbook Threat Model

!!! warning "Threat Model"
    OpenClaw agents often run with broad tool access. When connected to **Moltbook** or other agent networks, they can ingest untrusted, adversarial content that enables:

    - Prompt injection and hidden instruction attacks  
    - Tool misuse and policy bypass  
    - Behavioral drift over time  
    - Cascading cross‑agent exploitation  

    SuperClaw is built to evaluate these risks **before** deployment.

## Problem & Solution (Summary)

**Problem:** Agents are deployed with broad access, mutable behavior, and exposure to untrusted inputs, often without security validation. This leads to prompt injection, tool misuse, configuration drift, and data leakage discovered only after exposure.

**Solution:** SuperClaw performs **pre‑deployment, scenario‑driven security evaluation** of existing agents. It captures evidence (tool calls, outputs, artifacts), scores behavior against explicit contracts, and outputs actionable reports before agents touch sensitive data or external ecosystems.

**Non‑goals:** SuperClaw does **not** generate agents, run production workloads, or automate real‑world exploitation.

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

- [Installation Guide](getting-started/installation.md)
- [Quick Start Tutorial](getting-started/quickstart.md)
- [Architecture Overview](architecture/overview.md)
