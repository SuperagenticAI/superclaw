# Contributing

Thanks for your interest in contributing to SuperClaw!

## Development Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,docs]"
```

## Run Checks

```bash
ruff check .
ruff format --check .
pytest -q
```

## Pre-commit

```bash
pre-commit install
```

## Pull Requests
- Keep PRs focused and small.
- Add tests when you change behavior.
- Update docs if you change CLI or APIs.

## Reporting Security Issues
See [SECURITY.md](SECURITY.md).
