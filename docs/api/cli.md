# CLI Reference

Complete command-line interface reference for SuperClaw.

---

## Global Options

```bash
superclaw [OPTIONS] COMMAND [ARGS]
```

| Option | Description |
|--------|-------------|
| `--version` | Show version and exit |
| `--help` | Show help message |

---

## Commands

### attack

Run security attacks against an agent.

```bash
superclaw attack <adapter> [OPTIONS]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `adapter` | Target adapter: `openclaw`, `mock`, `acp` |

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--target` | Target URL | Config default |
| `--behaviors` | Comma-separated behaviors to test | `all` |
| `--techniques` | Comma-separated attack techniques | `all` |
| `--output` | Save results to file | None |
| `--dry-run` | Preview without executing | `false` |
| `--timeout` | Attack timeout in seconds | `30` |

**Examples:**

```bash
# Basic attack
superclaw attack openclaw --target ws://127.0.0.1:18789

# Specific behaviors
superclaw attack openclaw --behaviors prompt-injection-resistance,sandbox-isolation

# Save results
superclaw attack openclaw --output results.json

# Dry run
superclaw attack openclaw --dry-run
```

---

### generate

Generate attack scenarios using Bloom.

```bash
superclaw generate scenarios [OPTIONS]
```

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--behavior` | Behavior to generate scenarios for | Required |
| `--num-scenarios` | Number of scenarios to generate | `10` |
| `--variations` | Comma-separated variations | None |
| `--output` | Save scenarios to file | None |

**Examples:**

```bash
# Generate prompt injection scenarios
superclaw generate scenarios --behavior prompt_injection --num-scenarios 20

# With variations
superclaw generate scenarios --behavior jailbreak --variations noise,emotional_pressure

# Save to file
superclaw generate scenarios --behavior prompt_injection --output scenarios.json
```

---

### evaluate

Evaluate an agent against pre-generated scenarios.

```bash
superclaw evaluate <adapter> [OPTIONS]
```

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--scenarios` | Path to scenarios file | Required |
| `--behaviors` | Behaviors to evaluate | `all` |
| `--output` | Save results to file | None |

**Examples:**

```bash
superclaw evaluate openclaw --scenarios scenarios.json --behaviors all
superclaw evaluate mock --scenarios scenarios.json
```

---

### audit

Run a comprehensive security audit.

```bash
superclaw audit <adapter> [OPTIONS]
```

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--target` | Target URL | Config default |
| `--quick` | Quick audit (critical behaviors only) | `false` |
| `--comprehensive` | Full audit (all behaviors) | `false` |
| `--report-format` | Output format: `html`, `json`, `sarif` | `json` |
| `--output` | Output file path | `audit-report` |

**Examples:**

```bash
# Quick audit
superclaw audit openclaw --quick

# Comprehensive with HTML report
superclaw audit openclaw --comprehensive --report-format html --output report
```

---

### report

Generate and analyze reports.

```bash
superclaw report <subcommand> [OPTIONS]
```

**Subcommands:**

#### generate

Generate a report from results.

```bash
superclaw report generate --results <file> --format <format>
```

| Option | Description |
|--------|-------------|
| `--results` | Path to results JSON file |
| `--format` | Output format: `html`, `json`, `sarif` |
| `--output` | Output file path |

#### drift

Compare two runs for regressions.

```bash
superclaw report drift --baseline <file> --current <file>
```

| Option | Description |
|--------|-------------|
| `--baseline` | Path to baseline results |
| `--current` | Path to current results |
| `--output` | Output file path |

**Examples:**

```bash
# Generate SARIF for GitHub
superclaw report generate --results results.json --format sarif --output results.sarif

# Drift detection
superclaw report drift --baseline baseline.json --current current.json
```

---

### scan

Scan for security issues.

```bash
superclaw scan <subcommand> [OPTIONS]
```

**Subcommands:**

#### config

Scan SuperClaw configuration.

```bash
superclaw scan config [--output <file>]
```

#### skills

Scan agent skills/plugins for risky patterns.

```bash
superclaw scan skills --path <directory>
```

**Examples:**

```bash
superclaw scan config
superclaw scan skills --path /path/to/skills
```

---

### codeoptix

CodeOptiX integration commands.

```bash
superclaw codeoptix <subcommand> [OPTIONS]
```

**Subcommands:**

#### status

Check CodeOptiX integration status.

```bash
superclaw codeoptix status
```

#### register

Register SuperClaw behaviors with CodeOptiX.

```bash
superclaw codeoptix register
```

#### evaluate

Run multi-modal security evaluation.

```bash
superclaw codeoptix evaluate [OPTIONS]
```

| Option | Description | Default |
|--------|-------------|---------|
| `--target` | Target URL | Config default |
| `--llm-provider` | LLM provider | `openai` |
| `--behaviors` | Behaviors to evaluate | `all` |

**Examples:**

```bash
superclaw codeoptix status
superclaw codeoptix register
superclaw codeoptix evaluate --target ws://127.0.0.1:18789 --llm-provider anthropic
```

---

### Utility Commands

#### behaviors

List all available security behaviors.

```bash
superclaw behaviors
```

#### attacks

List all attack techniques.

```bash
superclaw attacks
```

#### init

Initialize configuration file.

```bash
superclaw init
```

Creates `~/.superclaw/config.yaml` with defaults.

---

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success / All behaviors passed |
| `1` | Critical or high severity findings detected |
| `2` | Connection or runtime error |

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SUPERCLAW_TARGET` | Default target URL |
| `SUPERCLAW_AUTH_TOKEN` | Authorization token for remote targets |
| `SUPERCLAW_LLM_PROVIDER` | LLM provider for Bloom |
| `SUPERCLAW_LOG_LEVEL` | Logging verbosity |
| `OPENAI_API_KEY` | OpenAI API key |
| `ANTHROPIC_API_KEY` | Anthropic API key |
