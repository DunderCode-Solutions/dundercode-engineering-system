# Repository Scripts

Repository automation is executed through `uv`.

The canonical local quality gate is:

```bash
bash scripts/quality.sh
```

The gate synchronizes locked dependencies, runs static checks and tests, validates metadata, generates and verifies all index artifacts, builds a wheel, and smoke-tests the installed commands in an isolated environment.

Do not bypass individual stages when validating a contribution.
