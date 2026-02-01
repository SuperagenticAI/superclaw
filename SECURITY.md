## Security and Ethical Use

SuperClaw is designed for **authorized security testing only**. By using this tool, you agree to the following:

### 1) Authorization Required
- Only test systems you own or have explicit, written permission to assess.
- Do **not** run attacks against public, third‑party, or production systems without consent.

### 2) Containment and Sandbox Isolation
- Run tests in **zero‑trust** environments (containers/VMs).
- Never execute tests directly on host machines with access to sensitive data.
- Use least‑privilege credentials and isolated test accounts.

### 3) False Positives and Human Review
- Scenario generation may produce **plausible but unrealistic** exploits.
- Treat findings as **signals**, not proof. Always validate manually.
- Do not claim vulnerabilities without confirming exploitability.

### 4) Data Safety
- Avoid testing with real secrets or personal data.
- Sanitize logs and reports before sharing.

### Reporting Issues
If you discover a security issue in SuperClaw itself, please open a GitHub issue with details and reproduction steps.
