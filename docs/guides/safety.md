# Safety & Guardrails

SuperClaw is **for authorized security testing only**. Do not use it against systems you do not own or explicitly have permission to test.

## Required Practices

- **Authorization**: Only test systems with written permission.
- **Containment**: Run tests in sandboxed/isolated environments (containers/VMs).
- **Validation**: Treat automated findings as signals and verify manually.

## Built-in Guardrails

SuperClaw enforces two runtime guardrails by default:

1. **Local-only mode**  
   Remote targets are blocked unless you explicitly allow them.

2. **Authorization for remote targets**  
   Remote targets require an auth token.

### Configure Guardrails

In `~/.superclaw/config.yaml`:

```yaml
safety:
  require_authorization: true
  local_only: true
```

Set a token for remote testing:

```bash
export SUPERCLAW_AUTH_TOKEN="your-token"
```

## False Positives

Scenario generation can produce plausible but unrealistic exploits. Always:
- Review evidence and context
- Reproduce critical findings manually
- Avoid over-reporting unverified results
