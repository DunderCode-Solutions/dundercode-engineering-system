"""
DESys Documentation Scanner

Scans the DESys repository and discovers Markdown documents.

Responsibilities:
    - Scan configured source directories
    - Ignore excluded directories
    - Return Markdown document paths

Author:
    DunderCode Engineering
"""

from __future__ import annotations

from pathlib import Path

from .config import IndexerConfig


def scan_markdown_documents(
    config: IndexerConfig,
    *,
    verbose: bool = False,
) -> list[Path]:
    """
    Scan all configured source directories and return Markdown documents.

    Parameters
    ----------
    config:
        DESys Indexer configuration.

    verbose:
        Enable verbose output.

    Returns
    -------
    list[Path]
        Sorted list of Markdown files.
    """

    documents: list[Path] = []

    for source in config.sources:
        if not source.exists():
            if verbose:
                print(f"[WARNING] Source not found: {source}")
            continue

        if verbose:
            print(f"[SCAN] {source}")

        documents.extend(
            _scan_directory(
                source=source,
                config=config,
                verbose=verbose,
            )
        )

    documents = sorted(set(documents))

    if verbose:
        print(f"[FOUND] {len(documents)} Markdown documents")

    return documents


# ---------------------------------------------------------------------
# Internal
# ---------------------------------------------------------------------


def _scan_directory(
    *,
    source: Path,
    config: IndexerConfig,
    verbose: bool,
) -> list[Path]:
    """
    Scan one source directory.
    """

    documents: list[Path] = []

    for file in source.rglob("*.md"):
        if _is_excluded(
            file=file,
            config=config,
        ):
            continue

        documents.append(file.resolve())

        if verbose:
            print(f"  + {file}")

    return documents


def _is_excluded(
    *,
    file: Path,
    config: IndexerConfig,
) -> bool:
    """
    Determine whether a file belongs to an excluded directory.
    """

    path_parts = set(file.parts)

    return any(
        excluded in path_parts
        for excluded in config.exclude
    )

