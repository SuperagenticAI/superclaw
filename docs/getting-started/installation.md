# Installation

## Requirements

- Python 3.12+
- pip or uv

## Installation Methods

### Using pip

```bash
pip install superclaw
```

### Using uv (Recommended)

```bash
uv pip install superclaw
```

### From Source

```bash
git clone https://github.com/SuperagenticAI/superclaw.git
cd superclaw
uv sync
```

### With Optional Dependencies

```bash
# With CodeOptiX integration
pip install superclaw[codeoptix]

# With development tools
pip install superclaw[dev]

# With documentation tools
pip install superclaw[docs]

# Everything
pip install superclaw[all]
```

## Verify Installation

```bash
superclaw version
superclaw behaviors
superclaw attacks
```

## UV Commands

```bash
# Sync dependencies
uv sync

# Run tests
uv run pytest

# Run CLI
uv run superclaw --help

# Build package
uv build
```
