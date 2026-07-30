"""
DESys Markdown Parser

Transforms Markdown documents into DESys domain models.

Responsibilities:
    - Read Markdown files
    - Extract metadata
    - Detect library
    - Build Document objects

Author:
    DunderCode Engineering
"""

from __future__ import annotations

from pathlib import Path

from .metadata import extract_metadata
from .models import Document, LibraryType


# =============================================================================
# Public API
# =============================================================================


def parse_document(
    path: Path,
) -> Document:
    """
    Parse a single Markdown document.

    Parameters
    ----------
    path
        Markdown document.

    Returns
    -------
    Document
    """

    markdown = _read_markdown(path)

    metadata = extract_metadata(markdown)

    document = Document(
        path=path.resolve(),
        library=_detect_library(path),
        metadata=metadata,
        title=_extract_title(markdown),
        summary=_extract_summary(markdown),
    )

    return document


def parse_documents(
    paths: list[Path],
) -> list[Document]:
    """
    Parse multiple Markdown documents.
    """

    return [
        parse_document(path)
        for path in sorted(paths)
    ]


# =============================================================================
# Internal
# =============================================================================


def _read_markdown(
    path: Path,
) -> str:
    """
    Read a Markdown document.
    """

    return path.read_text(
        encoding="utf-8",
    )


def _detect_library(
    path: Path,
) -> LibraryType:
    """
    Detect DESys library from the filesystem path.
    """

    parts = {
        part.lower()
        for part in path.parts
    }

    if "des" in parts:
        return LibraryType.DES

    if "dar" in parts:
        return LibraryType.DAR

    if "dea" in parts:
        return LibraryType.DEA

    if "dep" in parts:
        return LibraryType.DEP

    if "det" in parts:
        return LibraryType.DET

    if "dsk" in parts:
        return LibraryType.DSK

    if "dsp" in parts:
        return LibraryType.DSP

    return LibraryType.UNKNOWN


def _extract_title(
    markdown: str,
) -> str:
    """
    Extract the first Markdown heading.
    """

    for line in markdown.splitlines():

        line = line.strip()

        if line.startswith("# "):
            return line[2:].strip()

    return ""


def _extract_summary(
    markdown: str,
) -> str | None:
    """
    Extract a short document summary.

    Currently returns the first non-empty paragraph
    after the title.

    This implementation will evolve in future versions.
    """

    lines = markdown.splitlines()

    title_found = False

    paragraph: list[str] = []

    for line in lines:

        stripped = line.strip()

        if not title_found:

            if stripped.startswith("# "):
                title_found = True

            continue

        if not stripped:

            if paragraph:
                break

            continue

        if stripped.startswith("#"):
            break

        paragraph.append(stripped)

    if not paragraph:
        return None

    return " ".join(paragraph)

