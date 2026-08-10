"""Deterministic discovery of indexable DESys Markdown documents."""

from __future__ import annotations

from pathlib import Path

from tools.desys_indexer.config import IndexerConfig
from tools.desys_metadata import MANAGED_FILENAME_PATTERN


def scan_markdown_documents(config: IndexerConfig, *, verbose: bool = False) -> list[Path]:
    """Return non-empty managed Markdown files from configured sources."""
    documents: set[Path] = set()

    for source in config.sources:
        if verbose:
            print(f"[SCAN] {source.relative_to(config.repository_root).as_posix()}")
        for path in source.rglob("*.md"):
            if path.is_symlink() or not path.is_file():
                continue
            resolved = path.resolve()
            if not resolved.is_relative_to(config.repository_root):
                continue
            if config.is_excluded(resolved):
                continue
            if MANAGED_FILENAME_PATTERN.fullmatch(path.name) is None:
                continue
            if not path.read_text(encoding="utf-8").strip():
                continue
            documents.add(resolved)

    ordered = sorted(documents, key=lambda path: path.relative_to(config.repository_root).as_posix())
    if verbose:
        print(f"[FOUND] {len(ordered)} indexable documents")
    return ordered
