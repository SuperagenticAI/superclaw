# MVP Roadmap and Module Structure

This roadmap focuses on a small, usable SuperClaw MVP that can run behavior-driven security tests against agent targets, generate scenarios, and produce reports. It is structured to keep the core stable while enabling future extensions.

## MVP Goals (v0.1)

- Run behavior-driven attacks against a single target adapter (OpenClaw or mock)
- Generate scenario variants from a seed configuration
- Evaluate outcomes with a behavior scoring system
- Produce JSON and HTML reports with evidence and mitigations
- Enforce consent and local-only safety switches

## MVP Roadmap

### Phase 1: Core Execution

- CLI commands: `attack`, `audit`, `generate scenarios`
- Adapter interface: `connect`, `send_prompt`, `disconnect`
- Behavior registry with severity, score, evidence
- Basic reporting: JSON summary + per-behavior evidence

### Phase 2: Scenario Generation

- Seed format for behaviors, examples, variation dimensions
- Scenario builder (ideation + variations)
- Rollout runner to execute scenarios with the adapter
- Judgment hooks to score outcomes

### Phase 3: Reporting and Guardrails

- HTML report with grouped findings and mitigations
- SARIF scaffold (optional in MVP; wire in later)
- Safety gates: require authorization flag, local-only mode, rate limits

## Post-MVP Extensions

- Additional adapters: ACP, Claude Code, custom HTTP targets
- Supply-chain scanning: skills/plugins static checks
- Exposure scanning: open endpoints, weak auth, misconfigurations
- Compliance overlays: OWASP Agentic Top 10, NIST AI RMF
- Drift comparison: baseline vs modified agent behavior

## Proposed Module Structure

```
superclaw/
├── cli/                # CLI commands and option parsing
├── config/             # Settings, schemas, and defaults
├── adapters/           # Target adapters (OpenClaw, ACP, mock)
├── scenarios/          # Seed loading and scenario generation
├── attacks/            # Attack strategies and payload templates
├── behaviors/          # Behavior specs, scoring, severity levels
├── evaluation/         # Rollout orchestration and judgment hooks
├── reporting/          # JSON/HTML/SARIF report emitters
├── safety/             # Consent checks, local-only gates, rate limits
└── utils/              # Shared helpers
```

## Execution Flow (MVP)

1. Load config and seed behavior definitions
2. Generate scenarios (if requested)
3. Run attack rollouts through the adapter
4. Evaluate behaviors and score outcomes
5. Emit reports with evidence and mitigations

## MVP Artifacts

- `results.json` with behavior scores and evidence
- `report.html` with summaries and recommended mitigations
- `run.log` for auditability (optional for v0.1)
