---
hide:
  - toc
---

<div class="hero">
  <div class="hero__logo">
    <img src="assets/logo.png" alt="SuperClaw logo" />
  </div>
  <div class="hero__text">
    <h1>SuperClaw</h1>
    <p class="hero__tagline">Red‑Team AI Agents Before They Red‑Team You</p>
    <p class="hero__subtitle">Scenario‑driven, behavior‑first security testing for autonomous agents.</p>
    <div class="hero__cta">
      <a class="hero__button" href="getting-started/quickstart/">Get Started</a>
      <a class="hero__button hero__button--ghost" href="guides/attacks/">Run Your First Attack</a>
    </div>
  </div>
</div>

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

<div class="cards">
  <div class="card">
    <h3>Scenario‑Driven Testing</h3>
    <p>Generate adversarial scenarios and replay them against real agents.</p>
    <a href="getting-started/quickstart/">Learn more →</a>
  </div>
  <div class="card">
    <h3>Behavior Contracts</h3>
    <p>Explicit success criteria, evidence extraction, and mitigation guidance.</p>
    <a href="architecture/behaviors/">Explore behaviors →</a>
  </div>
  <div class="card">
    <h3>Evidence‑First Reporting</h3>
    <p>Reports include tool calls, outputs, and actionable fixes.</p>
    <a href="guides/attacks/">See reports →</a>
  </div>
  <div class="card">
    <h3>Guardrails</h3>
    <p>Local‑only mode and authorization checks to reduce misuse.</p>
    <a href="guides/safety/">Safety guide →</a>
  </div>
</div>
