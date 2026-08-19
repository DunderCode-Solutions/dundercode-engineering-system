# DESys v0.1 Pilot Defects

## PILOT-A-005 - Source File Without Terminal Newline Rejected

Severity: High
Status: Fixed and verified in rebuilt candidate
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

## PILOT-B-001 - Push Workflow Excludes Nonstandard Default Branch

Severity: High
Status: Fixed and verified in rebuilt candidate
Detected during: Pilot B remote CI preflight

### Environment

- Pilot: Pilot B, existing project
- Project default branch: `develop`
- DESys candidate: `30445a280e1210a158d93bf33e322258dbdf7167`
- Generated workflow: `.github/workflows/desys-docs-quality.yml`

### Reproduction

Initialize a repository whose default branch is neither `main` nor `master`.
The generated workflow contains:

```yaml
push:
  branches:
    - main
    - master
```

Committing and pushing the scaffold to the actual default branch does not
trigger the documentation job.

### Root Cause

The workflow template assumed two conventional default-branch names instead of
remaining independent from consumer branch policy.

### Correction

The generated workflow now accepts push events on every branch. Pull-request
and manual-dispatch behavior is unchanged. This avoids encoding consumer branch
governance into DESys.

### Regression Coverage

The initializer test now asserts that the generated workflow contains the push
event without a branch-name filter.

### Release Impact

Candidate `d959114699b19a0cb1aa9b4523bceeac6e8fcf0f` was rebuilt and installed in
Pilot B. The corrected workflow passed local dry-run, idempotency, and quality
gate verification. A push to Pilot B's default `develop` branch then triggered
successful GitHub Actions run `32257430389` automatically.
