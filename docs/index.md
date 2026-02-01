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

## What is SuperClaw?

SuperClaw is a **pre-deployment security testing framework** for AI coding agents. It systematically identifies vulnerabilities before your agents touch sensitive data or connect to external ecosystems.

<div class="cards">
  <div class="card">
    <h3>🎯 Scenario-Driven Testing</h3>
    <p>Generate and execute adversarial scenarios against real agents with reproducible results.</p>
    <a href="getting-started/quickstart/">Get started →</a>
  </div>
  <div class="card">
    <h3>📋 Behavior Contracts</h3>
    <p>Explicit success criteria, evidence extraction, and mitigation guidance for each security property.</p>
    <a href="architecture/behaviors/">Explore behaviors →</a>
  </div>
  <div class="card">
    <h3>📊 Evidence-First Reporting</h3>
    <p>Reports include tool calls, outputs, and actionable fixes in HTML, JSON, or SARIF formats.</p>
    <a href="guides/ci-cd/">CI/CD integration →</a>
  </div>
  <div class="card">
    <h3>🛡️ Built-in Guardrails</h3>
    <p>Local-only mode and authorization checks reduce misuse risk.</p>
    <a href="guides/safety/">Safety guide →</a>
  </div>
</div>

---

## ⚠️ Security and Ethical Use

!!! warning "Authorized Testing Only"
    SuperClaw is **for authorized security testing only**. Before using:
    
    - ✅ Obtain written permission to test the target system
    - ✅ Run tests in sandboxed or isolated environments
    - ✅ Treat automated findings as signals, not proof—verify manually

**Guardrails enforced by default:**

- Local-only mode blocks remote targets
- Remote targets require `SUPERCLAW_AUTH_TOKEN`

---

## Threat Model

!!! danger "OpenClaw + Moltbook Risk Surface"
    OpenClaw agents often run with broad tool access. When connected to **Moltbook** or other agent networks, they can ingest untrusted, adversarial content that enables:

    - **Prompt injection** and hidden instruction attacks  
    - **Tool misuse** and policy bypass  
    - **Behavioral drift** over time  
    - **Cascading cross-agent** exploitation  

    SuperClaw evaluates these risks **before** deployment.

### The Problem

Autonomous agents are deployed with **high privilege**, **mutable behavior**, and **exposure to untrusted inputs**—often without structured security validation. This makes prompt injection, tool misuse, configuration drift, and data leakage likely but poorly understood until after exposure.

### The Solution

SuperClaw performs **pre-deployment, scenario-driven security evaluation**:

1. **Generates** adversarial attack scenarios
2. **Executes** them against your agent
3. **Captures** evidence (tool calls, outputs, artifacts)
4. **Scores** behavior against explicit contracts
5. **Produces** actionable reports with mitigations

### Non-Goals

SuperClaw does **not**:

- Generate agents
- Run production workloads
- Automate real-world exploitation

---

## Quick Start

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

Run your first attack:

```bash
# Attack a local OpenClaw instance
superclaw attack openclaw --target ws://127.0.0.1:18789

# Or test offline with the mock adapter
superclaw attack mock --behaviors prompt-injection-resistance

# Generate a comprehensive audit report
superclaw audit openclaw --comprehensive --report-format html
```

---

## Key Features

| Feature | Description |
|---------|-------------|
| 🎯 **Attack Library** | 5 attack techniques with 100+ payloads |
| 🔍 **Behavior Specs** | 6 security behaviors with severity levels |
| 🌸 **Bloom Integration** | LLM-powered scenario generation |
| 📊 **Multi-Format Reports** | HTML, JSON, SARIF for CI/CD |
| 🔬 **CodeOptiX Integration** | Multi-modal evaluation pipeline |

### Supported Targets

| Target | Adapter | Description |
|--------|---------|-------------|
| 🦞 **OpenClaw** | `openclaw` | AI coding agents via ACP WebSocket |
| 🧪 **Mock** | `mock` | Offline deterministic testing |
| 🔧 **Custom** | Extend `BaseAdapter` | Build your own adapter |

### Attack Techniques

| Technique | Description |
|-----------|-------------|
| `prompt-injection` | Direct and indirect injection attacks |
| `encoding` | Base64, hex, unicode, typoglycemia obfuscation |
| `jailbreak` | DAN, grandmother, role-play bypass techniques |
| `tool-bypass` | Tool policy bypass via alias confusion |
| `multi-turn` | Persistent escalation across conversation turns |

### Security Behaviors

| Behavior | Severity | Tests |
|----------|----------|-------|
| `prompt-injection-resistance` | 🔴 CRITICAL | Injection detection and rejection |
| `sandbox-isolation` | 🔴 CRITICAL | Container and filesystem boundaries |
| `tool-policy-enforcement` | 🟠 HIGH | Allow/deny list compliance |
| `session-boundary-integrity` | 🟠 HIGH | Cross-session isolation |
| `configuration-drift-detection` | 🟡 MEDIUM | Config stability over time |
| `acp-protocol-security` | 🟡 MEDIUM | Protocol message handling |

---

## Superagentic AI Ecosystem

SuperClaw is part of a comprehensive AI quality and security ecosystem:

```
┌─────────────────────────────────────────────────────────────┐
│                  Superagentic AI Ecosystem                  │
├─────────────────────────────────────────────────────────────┤
│  SuperQE      │  Quality Engineering core engine            │
│  SuperClaw    │  Agent security testing framework ◄── YOU   │
│  CodeOptiX    │  Code optimization & evaluation engine      │
│  Bloom        │  Behavioral evaluation scenario generation  │
└─────────────────────────────────────────────────────────────┘
```

---

## Next Steps

<div class="cards">
  <div class="card">
    <h3>📦 Installation</h3>
    <p>Get SuperClaw set up with pip, uv, or from source.</p>
    <a href="getting-started/installation/">Install now →</a>
  </div>
  <div class="card">
    <h3>⚡ Quick Start</h3>
    <p>Run your first security scan in under 5 minutes.</p>
    <a href="getting-started/quickstart/">Quick start →</a>
  </div>
  <div class="card">
    <h3>🏗️ Architecture</h3>
    <p>Understand how SuperClaw works under the hood.</p>
    <a href="architecture/overview/">Learn more →</a>
  </div>
  <div class="card">
    <h3>🔄 CI/CD</h3>
    <p>Integrate security scanning into your pipeline.</p>
    <a href="guides/ci-cd/">Set up CI/CD →</a>
  </div>
</div>
