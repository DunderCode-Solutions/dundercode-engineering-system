# DESys v0.1 Pilot Defects

## PILOT-A-005 - Source File Without Terminal Newline Rejected

Severity: High  
Status: Fixed, candidate rebuild required  
Detected during: `PKG-006` cold/warm quality-gate measurement

### Environment

- Pilot: Pilot A, new project
- DESys candidate: `09aaec62fc5183ed19f30d13b73f39301812bd8d`
- Tool source: repository-relative wheel
- `uv`: 0.12.3
- Host: Linux x86_64

### Reproduction

`tools/desys-source.txt` contained exactly one valid wheel path without a
terminal newline. Running:

```bash
bash scripts/desys-docs-quality.sh
```

returned:

```text
ERROR: DESys source file must contain exactly one non-empty line.
```

### Root Cause

Bash `read` assigns the final unterminated line but returns a non-zero status at
EOF. The generated script treated that status as an empty or invalid source and
discarded the assigned value.

### Correction

The generated script now accepts exactly one non-empty source line with or
without a terminal newline. It continues to reject empty and multiple-line
source files before invoking `uvx`.

### Regression Coverage

- one valid source line with terminal newline;
- one valid source line without terminal newline;
- multiple source lines;
- malformed or mutable source values.

### Release Impact

The affected candidate must not be used for final packaging evidence. Generate
a new commit and wheel, update the Pilot A scaffold, and repeat `PKG-001`
through `PKG-006`.
