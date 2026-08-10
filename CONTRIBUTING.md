# Contributing to DESys

DESys treats documentation, metadata, tooling, and generated knowledge indexes as engineering assets.

# Prerequisites

- Git
- `uv` 0.12.3 or compatible
- Python 3.12, managed through `uv`

# Environment

Create or synchronize the locked development environment:

```bash
uv sync --locked --group dev
```

Dependency changes MUST update `pyproject.toml` and `uv.lock` together:

```bash
uv lock
```

# Quality Gate

Run the complete local gate before submitting a change:

```bash
bash scripts/quality.sh
```

The gate performs:

- Ruff static checks.
- Pytest unit and integration tests.
- Canonical metadata validation.
- Deterministic index rendering.
- Generation and cross-validation of all five index artifacts.
- Wheel build and isolated installation smoke tests.

# Metadata Changes

Every non-empty, identifier-bearing Markdown document MUST use the canonical metadata contract defined by DEKG-0040.

Validate metadata independently with:

```bash
uv run desys-metadata-validate
```

Warnings represent governed technical debt. The quality gate enforces the current maximum baseline of 127 warnings, so new warnings cannot be introduced without an explicit governance change.

# Index Changes

Validate index generation without writing:

```bash
uv run desys-build-index --dry-run
```

Generate and verify artifacts:

```bash
uv run desys-build-index
uv run desys-check-indexes
```

Generated files under `skills/generated/` are local build artifacts and are not committed.

# Project Initializer Changes

Preview the consumer project scaffold with:

```bash
uv run desys-project-init --root <consumer-repository> --dry-run
```

Initializer changes MUST preserve non-destructive preflight behavior,
deterministic output, idempotency, and compatibility with the generated
consumer quality gate. Existing `AGENTS.md` content MUST be preserved outside
the managed DESys instruction markers.

# Pull Requests

Pull requests SHOULD:

- explain the engineering problem and intended outcome;
- identify affected canonical documents;
- include tests for tooling behavior changes;
- pass the complete quality gate;
- avoid combining unrelated structural and editorial changes.
