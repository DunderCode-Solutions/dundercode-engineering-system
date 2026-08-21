"""Canonical front matter parser for DESys index documents."""

from __future__ import annotations

import re
from pathlib import Path, PurePosixPath

from tools.desys_indexer.models import IndexedDocument
from tools.desys_metadata import FrontMatterError, parse_front_matter, validate_document_metadata

HEADING_PATTERN = re.compile(r"^#{1,6}\s+(.+?)\s*$")


class IndexingError(ValueError):
    """Raised when a document cannot safely enter generated indexes."""


def parse_document(path: Path, *, repository_root: Path) -> IndexedDocument:
    """Parse one validated Markdown document into the index model."""
    resolved = path.resolve()
    root = repository_root.resolve()
    if not resolved.is_relative_to(root):
        raise IndexingError(f"Document is outside repository root: {path}")

    relative_path = resolved.relative_to(root)
    markdown = resolved.read_text(encoding="utf-8")
    try:
        metadata, body = parse_front_matter(markdown)
    except FrontMatterError as error:
        raise IndexingError(f"{relative_path.as_posix()}: {error}") from error

    errors = [
        issue
        for issue in validate_document_metadata(metadata, relative_path)
        if issue.severity == "error"
    ]
    if errors:
        messages = "; ".join(issue.message for issue in errors)
        raise IndexingError(f"{relative_path.as_posix()}: {messages}")

    normalized_body = body.replace("\r\n", "\n").replace("\r", "\n").lstrip("\n")
    headings = tuple(
        match.group(1)
        for line in normalized_body.splitlines()
        if (match := HEADING_PATTERN.match(line)) is not None
    )

    return IndexedDocument(
        path=PurePosixPath(relative_path.as_posix()),
        metadata=metadata,
        body=normalized_body,
        headings=headings,
        summary=_extract_summary(normalized_body),
    )


def parse_documents(paths: list[Path], *, repository_root: Path) -> list[IndexedDocument]:
    """Parse documents in stable repository path order."""
    documents = [parse_document(path, repository_root=repository_root) for path in paths]
    return sorted(documents, key=lambda document: document.canonical_id)


def _extract_summary(body: str) -> str | None:
    paragraph: list[str] = []
    in_fence = False
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not stripped or stripped.startswith("#"):
            if paragraph:
                break
            continue
        paragraph.append(stripped)

    if not paragraph:
        return None
    summary = " ".join(paragraph)
    return summary if len(summary) <= 500 else f"{summary[:497].rstrip()}..."
