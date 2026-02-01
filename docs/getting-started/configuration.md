# Configuration

## Initialize Config

```bash
superclaw init
```

Creates `~/.superclaw/config.yaml`.

## Config File Structure

```yaml
# ~/.superclaw/config.yaml

# Default target for attacks
default_target: "ws://127.0.0.1:18789"

# LLM settings for Bloom scenario generation
llm:
  provider: "anthropic"  # openai, anthropic, google, ollama
  model: "claude-sonnet-4"

# Logging
logging:
  level: "INFO"
  file: "~/.superclaw/superclaw.log"

# Safety settings
safety:
  require_authorization: true
  local_only: true
  max_concurrent_attacks: 5
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SUPERCLAW_TARGET` | Default target URL |
| `SUPERCLAW_LLM_PROVIDER` | LLM provider (openai, anthropic) |
| `OPENAI_API_KEY` | OpenAI API key |
| `ANTHROPIC_API_KEY` | Anthropic API key |

## LLM Provider Setup

### OpenAI

```bash
export OPENAI_API_KEY="sk-..."
superclaw generate scenarios --behavior prompt_injection
```

### Anthropic

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
superclaw codeoptix evaluate --llm-provider anthropic
```
