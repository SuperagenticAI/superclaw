# CI/CD Integration

## GitHub Actions

```yaml
name: Security Scan

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    
    services:
      openclaw:
        image: superagentic/openclaw:latest
        ports:
          - 18789:18789
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      
      - name: Install SuperClaw
        run: pip install superclaw
      
      - name: Run Security Scan
        run: |
          superclaw audit openclaw \
            --target ws://localhost:18789 \
            --comprehensive \
            --report-format sarif \
            --output security-results
      
      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: security-results.sarif
      
      - name: Check for Critical Findings
        run: |
          if grep -q '"level": "error"' security-results.sarif; then
            echo "Critical security findings detected!"
            exit 1
          fi
```

## GitLab CI

```yaml
security-scan:
  stage: test
  image: python:3.12
  script:
    - pip install superclaw
    - superclaw audit openclaw --report-format json --output results.json
  artifacts:
    reports:
      security: results.json
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All behaviors passed |
| 1 | Critical/High findings detected |
| 2 | Connection error |

## SARIF Output

SuperClaw generates SARIF 2.1.0 format compatible with:

- GitHub Code Scanning
- Azure DevOps
- SonarQube
- Other SARIF consumers
