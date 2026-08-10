"""Initialize DESys documentation tooling in a consumer Git repository."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as distribution_version
from pathlib import Path, PurePosixPath
from tempfile import NamedTemporaryFile

PACKAGE_NAME = "dundercode-engineering-system"

MANAGED_DIRECTORIES = (
    PurePosixPath(".github"),
    PurePosixPath(".github/workflows"),
    PurePosixPath("docs"),
    PurePosixPath("docs/adr"),
    PurePosixPath("docs/desys"),
    PurePosixPath("docs/prd"),
    PurePosixPath("docs/rfc"),
    PurePosixPath("scripts"),
    PurePosixPath("tools"),
)

IGNORE_PATH = PurePosixPath(".gitignore")
IGNORE_RULE = b"/docs/generated/"
IGNORE_BEGIN = b"# BEGIN DESys generated artifacts"
IGNORE_END = b"# END DESys generated artifacts"
IGNORE_BLOCK_LINES = (IGNORE_BEGIN, IGNORE_RULE, IGNORE_END)

AGENTS_PATH = PurePosixPath("AGENTS.md")
AGENTS_BEGIN = b"<!-- BEGIN DESys documentation instructions -->"
AGENTS_END = b"<!-- END DESys documentation instructions -->"
AGENTS_BLOCK = """<!-- BEGIN DESys documentation instructions -->
## DESys Documentation Instructions

This repository uses DESys documentation as engineering context.

Before changing requirements, architecture, or cross-cutting behavior:

1. Review relevant documents under `docs/adr/`, `docs/prd/`, and `docs/rfc/`.
2. Use `docs/generated/search-index.json` to discover related documents when
   the generated index is available.
3. Open the source path recorded by the index; source Markdown is authoritative.
4. Prefer approved or published decisions over drafts and report conflicts
   instead of silently bypassing documented constraints.

When engineering behavior changes:

1. Update or create the corresponding ADR, PRD, or RFC.
2. Do not edit files under `docs/generated/` manually.
3. Run `bash scripts/desys-docs-quality.sh` before considering the change
   complete.
<!-- END DESys documentation instructions -->
"""
AGENTS_BLOCK_LINES = tuple(AGENTS_BLOCK.encode("utf-8").splitlines())

INDEXER_CONFIG = """version: 1

repository_root: ..

sources:
  - docs/adr
  - docs/prd
  - docs/rfc

output_directory: docs/generated

exclude:
  - .git
  - .venv
  - __pycache__
  - node_modules
  - build
  - dist
  - site
  - docs/generated

artifacts:
  - index.yaml
  - graph.yaml
  - navigation.yaml
  - aliases.yaml
  - search-index.json
"""

QUALITY_SCRIPT = """#!/usr/bin/env bash
set -euo pipefail

script_directory="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repository_root="$(git -C "$script_directory/.." rev-parse --show-toplevel)"
cd "$repository_root"

uv run --locked --group desys desys-build-index \\
  --dry-run \\
  --config tools/desys_indexer.yaml

uv run --locked --group desys desys-build-index \\
  --config tools/desys_indexer.yaml

uv run --locked --group desys desys-check-indexes \\
  --output docs/generated
"""

QUALITY_WORKFLOW = """name: DESys Documentation Quality

on:
  pull_request:
  push:
    branches:
      - main
      - master
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: desys-docs-${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: true

jobs:
  documentation:
    name: Documentation
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - name: Checkout
        uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4
        with:
          persist-credentials: false

      - name: Set up Python
        uses: actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065 # v5
        with:
          python-version: "3.12"

      - name: Set up uv
        uses: astral-sh/setup-uv@d0cc045d04ccac9d8b7881df0226f9e82c39688e # v6
        with:
          version: "0.12.3"
          enable-cache: true
          cache-dependency-glob: uv.lock

      - name: Synchronize DESys tooling
        run: uv sync --locked --group desys

      - name: Run documentation quality gate
        run: bash scripts/desys-docs-quality.sh

      - name: Minimize cached data
        if: always()
        run: uv cache prune --ci
"""


class ProjectInitializationError(RuntimeError):
    """Raised when a consumer repository cannot be safely initialized."""


@dataclass(frozen=True, slots=True)
class PlannedOperation:
    action: str
    path: PurePosixPath
    content: bytes | None = None
    reason: str | None = None
    is_directory: bool = False


@dataclass(frozen=True, slots=True)
class InitializationPlan:
    operations: tuple[PlannedOperation, ...]

    @property
    def has_conflicts(self) -> bool:
        return any(operation.action == "CONFLICT" for operation in self.operations)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Consumer Git repository root. Defaults to the current directory.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and print the initialization plan without writing files.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {_installed_version()}",
    )
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    try:
        plan = initialize_project(arguments.root, dry_run=arguments.dry_run)
    except ProjectInitializationError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    for operation in plan.operations:
        suffix = f" ({operation.reason})" if operation.reason else ""
        print(f"{operation.action:<9} {operation.path.as_posix()}{suffix}")

    if plan.has_conflicts:
        print("Initialization aborted because managed paths conflict.", file=sys.stderr)
        return 1
    if arguments.dry_run:
        print("Dry run completed; no files were written.")
    else:
        changed = sum(operation.action in {"CREATE", "UPDATE"} for operation in plan.operations)
        print(f"DESys project integration initialized ({changed} path(s) changed).")
    return 0


def initialize_project(
    root: Path,
    *,
    dry_run: bool = False,
    version: str | None = None,
) -> InitializationPlan:
    """Plan and optionally apply a safe DESys consumer scaffold."""
    root = _validate_repository_root(root)
    files = _render_project_files(version or _installed_version())
    operations = [
        _classify_directory(root, path)
        for path in MANAGED_DIRECTORIES
    ]
    operations.extend(
        _classify_file(root, path, content)
        for path, content in files.items()
    )
    operations.append(_classify_agents(root))
    operations.append(_classify_gitignore(root))
    plan = InitializationPlan(tuple(sorted(operations, key=lambda operation: operation.path.as_posix())))

    if plan.has_conflicts or dry_run:
        return plan

    try:
        for operation in sorted(
            (item for item in plan.operations if item.action == "CREATE" and item.is_directory),
            key=lambda item: (len(item.path.parts), item.path.as_posix()),
        ):
            (root / operation.path).mkdir()
        for operation in plan.operations:
            if operation.is_directory or operation.action not in {"CREATE", "UPDATE"}:
                continue
            destination = root / operation.path
            if operation.content is None:
                raise ProjectInitializationError(f"No rendered content for {operation.path}")
            if operation.action == "CREATE":
                with destination.open("xb") as stream:
                    stream.write(operation.content)
            else:
                _replace_file(destination, operation.content)
    except OSError as error:
        raise ProjectInitializationError(f"Unable to apply initialization plan: {error}") from error

    return plan


def _validate_repository_root(root: Path) -> Path:
    try:
        resolved = root.expanduser().resolve(strict=True)
    except OSError as error:
        raise ProjectInitializationError(f"Repository root does not exist: {root}") from error
    if not resolved.is_dir():
        raise ProjectInitializationError(f"Repository root is not a directory: {root}")
    git_entry = resolved / ".git"
    if git_entry.is_symlink() or not git_entry.exists():
        raise ProjectInitializationError("Repository root must contain a non-symlinked .git entry.")
    if not (git_entry.is_dir() or git_entry.is_file()):
        raise ProjectInitializationError("Repository .git entry must be a file or directory.")
    try:
        result = subprocess.run(
            ["git", "-C", str(resolved), "rev-parse", "--show-toplevel"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as error:
        raise ProjectInitializationError(f"Unable to inspect Git repository: {error}") from error
    if result.returncode != 0:
        message = result.stderr.strip() or "git rev-parse failed"
        raise ProjectInitializationError(f"Repository root is not a Git worktree: {message}")
    try:
        git_root = Path(result.stdout.strip()).resolve(strict=True)
    except OSError as error:
        raise ProjectInitializationError("Git returned an invalid repository root.") from error
    if git_root != resolved:
        raise ProjectInitializationError("--root must identify the Git worktree root itself.")
    return resolved


def _classify_directory(root: Path, relative: PurePosixPath) -> PlannedOperation:
    destination = root / relative
    unsafe_ancestor = _unsafe_ancestor(root, relative)
    if unsafe_ancestor is not None:
        return PlannedOperation("CONFLICT", relative, reason=unsafe_ancestor, is_directory=True)
    if destination.is_symlink():
        return PlannedOperation("CONFLICT", relative, reason="managed directory is a symlink", is_directory=True)
    if not destination.exists():
        return PlannedOperation("CREATE", relative, is_directory=True)
    if not destination.is_dir():
        return PlannedOperation("CONFLICT", relative, reason="expected a directory", is_directory=True)
    return PlannedOperation("UNCHANGED", relative, is_directory=True)


def _classify_file(root: Path, relative: PurePosixPath, content: bytes) -> PlannedOperation:
    destination = root / relative
    unsafe_ancestor = _unsafe_ancestor(root, relative)
    if unsafe_ancestor is not None:
        return PlannedOperation("CONFLICT", relative, reason=unsafe_ancestor)
    if destination.is_symlink():
        return PlannedOperation("CONFLICT", relative, reason="managed file is a symlink")
    if not destination.exists():
        return PlannedOperation("CREATE", relative, content=content)
    if not destination.is_file():
        return PlannedOperation("CONFLICT", relative, reason="expected a file")
    try:
        current = destination.read_bytes()
    except OSError as error:
        return PlannedOperation("CONFLICT", relative, reason=f"cannot read managed file: {error}")
    if current == content:
        return PlannedOperation("UNCHANGED", relative)
    return PlannedOperation("CONFLICT", relative, reason="existing content differs")


def _classify_gitignore(root: Path) -> PlannedOperation:
    destination = root / IGNORE_PATH
    if destination.is_symlink():
        return PlannedOperation("CONFLICT", IGNORE_PATH, reason="managed file is a symlink")
    if not destination.exists():
        return PlannedOperation("CREATE", IGNORE_PATH, content=_ignore_block(b"\n"))
    if not destination.is_file():
        return PlannedOperation("CONFLICT", IGNORE_PATH, reason="expected a file")
    try:
        current = destination.read_bytes()
    except OSError as error:
        return PlannedOperation("CONFLICT", IGNORE_PATH, reason=f"cannot read managed file: {error}")

    lines = current.splitlines()
    block_positions = [
        index
        for index in range(max(0, len(lines) - 2))
        if tuple(lines[index : index + 3]) == IGNORE_BLOCK_LINES
    ]
    contains_marker = IGNORE_BEGIN in current or IGNORE_END in current
    if len(block_positions) == 1 and lines.count(IGNORE_BEGIN) == 1 and lines.count(IGNORE_END) == 1:
        return PlannedOperation("UNCHANGED", IGNORE_PATH)
    if contains_marker:
        return PlannedOperation("CONFLICT", IGNORE_PATH, reason="DESys ignore markers are malformed")
    if any(line.strip() == IGNORE_RULE for line in lines):
        return PlannedOperation("UNCHANGED", IGNORE_PATH)

    newline = b"\r\n" if b"\r\n" in current else b"\n"
    if not current:
        updated = _ignore_block(newline)
    elif current.endswith(newline * 2):
        updated = current + _ignore_block(newline)
    elif current.endswith(newline):
        updated = current + newline + _ignore_block(newline)
    else:
        updated = current + newline * 2 + _ignore_block(newline)
    return PlannedOperation("UPDATE", IGNORE_PATH, content=updated)


def _classify_agents(root: Path) -> PlannedOperation:
    destination = root / AGENTS_PATH
    if destination.is_symlink():
        return PlannedOperation("CONFLICT", AGENTS_PATH, reason="managed file is a symlink")
    if not destination.exists():
        return PlannedOperation("CREATE", AGENTS_PATH, content=AGENTS_BLOCK.encode("utf-8"))
    if not destination.is_file():
        return PlannedOperation("CONFLICT", AGENTS_PATH, reason="expected a file")
    try:
        current = destination.read_bytes()
    except OSError as error:
        return PlannedOperation("CONFLICT", AGENTS_PATH, reason=f"cannot read managed file: {error}")

    lines = current.splitlines()
    block_size = len(AGENTS_BLOCK_LINES)
    block_positions = [
        index
        for index in range(max(0, len(lines) - block_size + 1))
        if tuple(lines[index : index + block_size]) == AGENTS_BLOCK_LINES
    ]
    contains_marker = AGENTS_BEGIN in current or AGENTS_END in current
    if len(block_positions) == 1 and lines.count(AGENTS_BEGIN) == 1 and lines.count(AGENTS_END) == 1:
        return PlannedOperation("UNCHANGED", AGENTS_PATH)
    if contains_marker:
        return PlannedOperation("CONFLICT", AGENTS_PATH, reason="DESys agent instruction markers are malformed")

    newline = b"\r\n" if b"\r\n" in current else b"\n"
    block = newline.join(AGENTS_BLOCK_LINES) + newline
    if not current:
        updated = block
    elif current.endswith(newline * 2):
        updated = current + block
    elif current.endswith(newline):
        updated = current + newline + block
    else:
        updated = current + newline * 2 + block
    return PlannedOperation("UPDATE", AGENTS_PATH, content=updated)


def _unsafe_ancestor(root: Path, relative: PurePosixPath) -> str | None:
    current = root
    for part in relative.parts[:-1]:
        current /= part
        if current.is_symlink():
            return f"ancestor is a symlink: {current.relative_to(root).as_posix()}"
        if current.exists() and not current.is_dir():
            return f"ancestor is not a directory: {current.relative_to(root).as_posix()}"
    return None


def _ignore_block(newline: bytes) -> bytes:
    return newline.join(IGNORE_BLOCK_LINES) + newline


def _replace_file(destination: Path, content: bytes) -> None:
    """Atomically replace a managed file while preserving its permission mode."""
    temporary_path: Path | None = None
    mode = destination.stat().st_mode
    try:
        with NamedTemporaryFile(mode="wb", dir=destination.parent, prefix=f".{destination.name}.", delete=False) as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
            temporary_path = Path(stream.name)
        os.chmod(temporary_path, mode)
        os.replace(temporary_path, destination)
        temporary_path = None
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def _installed_version() -> str:
    try:
        return distribution_version(PACKAGE_NAME)
    except PackageNotFoundError:
        return "unreleased"


def _render_project_files(version: str) -> dict[PurePosixPath, bytes]:
    if not version.strip():
        raise ProjectInitializationError("DESys version must not be empty.")
    text_files = {
        PurePosixPath(".github/workflows/desys-docs-quality.yml"): QUALITY_WORKFLOW,
        PurePosixPath("docs/adr/README.md"): _collection_readme("Architecture Decisions", "ADR"),
        PurePosixPath("docs/desys/README.md"): _integration_readme(version),
        PurePosixPath("docs/prd/README.md"): _collection_readme("Product Requirements", "PRD"),
        PurePosixPath("docs/rfc/README.md"): _collection_readme("Engineering Proposals", "RFC"),
        PurePosixPath("scripts/desys-docs-quality.sh"): QUALITY_SCRIPT,
        PurePosixPath("tools/desys_indexer.yaml"): INDEXER_CONFIG,
    }
    return {
        path: content.encode("utf-8")
        for path, content in sorted(text_files.items(), key=lambda item: item[0].as_posix())
    }


def _collection_readme(title: str, prefix: str) -> str:
    return f"""# {title}

Store canonical `{prefix}` documents in this directory.

Indexable documents must use DESys YAML front matter and filenames beginning
with `{prefix}-` followed by a four-digit identifier, for example
`{prefix}-0001-example.md`.

This `README.md` is a navigation surface and is not indexed as a DEKG node.
"""


def _integration_readme(version: str) -> str:
    return f"""# DESys Project Integration

This project scaffold was generated with DESys `{version}` and requires Python
3.12 and `uv`.

## Dependency

Add DESys to a dedicated dependency group and commit both `pyproject.toml` and
`uv.lock`:

```bash
uv add --group desys "dundercode-engineering-system=={version}"
uv lock
```

Until a package release is available, use an immutable Git revision instead:

```bash
uv add --group desys \\
  "dundercode-engineering-system @ git+<DESYS_REPOSITORY_URL>@<FULL_COMMIT_SHA>"
uv lock
```

Do not use an unpinned branch as the project dependency source.

## Quality Gate

Synchronize the locked environment and run the documentation gate:

```bash
uv sync --locked --group desys
bash scripts/desys-docs-quality.sh
```

The gate validates canonical metadata, renders the project documentation, and
checks `index.yaml`, `graph.yaml`, `navigation.yaml`, `aliases.yaml`, and
`search-index.json` under `docs/generated/`.

The `docs/generated/` directory is owned by DESys. Its five index artifacts are
replaced whenever the quality gate runs; do not store source documents there.

The root `AGENTS.md` provides vendor-neutral instructions for AI agents to
discover and respect this documentation. It does not install or activate DESys
skills.
"""


if __name__ == "__main__":
    raise SystemExit(main())
