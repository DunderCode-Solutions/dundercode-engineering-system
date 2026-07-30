"""
DESys Metadata Parser

Extracts and validates the Metadata section from
DESys Markdown documents.

Author:
    DunderCode Engineering
"""

from __future__ import annotations

import re

from .models import (
    CanonicalIdentifier,
    DocumentMetadata,
)


# =============================================================================
# Exceptions
# =============================================================================


class MetadataError(Exception):
    """Raised when document metadata is invalid."""


# =============================================================================
# Constants
# =============================================================================


_REQUIRED_FIELDS = (
    "Document Number",
    "Canonical ID",
    "Document Class",
    "Version",
    "Status",
    "Canonical Language",
    "Owner",
)


_METADATA_HEADER_PATTERN = re.compile(
    r"^\s*#\s*Metadata\s*$",
    flags=re.IGNORECASE | re.MULTILINE,
)


_METADATA_FIELD_PATTERN = re.compile(
    r"^([A-Za-z][A-Za-z\s]+):\s*(.+?)\s*$",
    flags=re.MULTILINE,
)


_SECTION_HEADER_PATTERN = re.compile(
    r"^\s*#",
)


# =============================================================================
# Public API
# =============================================================================


def extract_metadata(
    markdown: str,
) -> DocumentMetadata:
    """
    Extract metadata from a DESys Markdown document.

    Parameters
    ----------
    markdown
        Complete Markdown document.

    Returns
    -------
    DocumentMetadata

    Raises
    ------
    MetadataError
    """

    block = _find_metadata_block(markdown)

    fields = _parse_metadata_block(block)

    _validate_metadata(fields)

    return _build_metadata(fields)


# =============================================================================
# Internal
# =============================================================================


def _find_metadata_block(
    markdown: str,
) -> str:
    """
    Locate the Metadata block.
    """

    match = _METADATA_HEADER_PATTERN.search(markdown)

    if match is None:
        raise MetadataError(
            "Metadata section not found."
        )

    remaining = markdown[match.end():]

    lines = remaining.splitlines()

    collected: list[str] = []

    for line in lines:

        stripped = line.strip()

        # End by explicit separator
        if stripped == "---":
            break

        # End by next heading
        if _SECTION_HEADER_PATTERN.match(stripped):
            break

        # End by blank line after content
        if not stripped:
            if collected:
                break
            continue

        collected.append(line)

    if not collected:
        raise MetadataError(
            "Metadata section is empty."
        )

    return "\n".join(collected)


def _parse_metadata_block(
    block: str,
) -> dict[str, str]:
    """
    Parse Metadata block into a dictionary.
    """

    metadata: dict[str, str] = {}

    for key, value in _METADATA_FIELD_PATTERN.findall(block):

        metadata[key.strip()] = value.strip()

    return metadata


def _validate_metadata(
    metadata: dict[str, str],
) -> None:
    """
    Validate required metadata fields.
    """

    for field in _REQUIRED_FIELDS:

        if field not in metadata:

            raise MetadataError(
                f"Missing metadata field '{field}'."
            )

        if not metadata[field]:

            raise MetadataError(
                f"Metadata field '{field}' is empty."
            )


def _build_metadata(
    metadata: dict[str, str],
) -> DocumentMetadata:
    """
    Build a DocumentMetadata instance.
    """

    return DocumentMetadata(

        document_number=metadata["Document Number"],

        canonical_id=CanonicalIdentifier.from_string(
            metadata["Canonical ID"]
        ),

        document_class=metadata["Document Class"],

        version=metadata["Version"],

        status=metadata["Status"],

        canonical_language=metadata["Canonical Language"],

        owner=metadata["Owner"],
    )