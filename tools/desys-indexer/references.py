"""
DESys Reference Parser

Extracts cross-document references from DESys Markdown documents.

Responsibilities:
    - Locate reference sections
    - Parse Canonical IDs
    - Build Reference objects

Author:
    DunderCode Engineering
"""

from __future__ import annotations

from collections.abc import Iterable

from .models import (
    CanonicalIdentifier,
    Reference,
    RelationType,
)


# =============================================================================
# Constants
# =============================================================================

_REFERENCE_SECTIONS: dict[str, RelationType] = {
    "Related Documents": RelationType.RELATED,
    "References": RelationType.REFERENCES,
    "Depends On": RelationType.DEPENDS_ON,
    "Parent": RelationType.PARENT,
    "Children": RelationType.CHILD,
}


# =============================================================================
# Public API
# =============================================================================


def extract_references(
    markdown: str,
    source: CanonicalIdentifier,
) -> list[Reference]:
    """
    Extract references from a DESys Markdown document.

    Parameters
    ----------
    markdown
        Markdown document.

    source
        Source document canonical identifier.

    Returns
    -------
    list[Reference]
    """

    references: list[Reference] = []

    for title, relation in _REFERENCE_SECTIONS.items():

        identifiers = _extract_section(
            markdown=markdown,
            section=title,
        )

        references.extend(
            _build_references(
                source=source,
                identifiers=identifiers,
                relation=relation,
            )
        )

    return references


# =============================================================================
# Internal
# =============================================================================


def _extract_section(
    *,
    markdown: str,
    section: str,
) -> list[str]:
    """
    Extract Canonical IDs from one section.
    """

    lines = markdown.splitlines()

    inside = False

    identifiers: list[str] = []

    expected_heading = f"## {section}"

    for line in lines:

        stripped = line.strip()

        if not inside:

            if stripped == expected_heading:
                inside = True

            continue

        if stripped.startswith("#"):
            break

        if not stripped:
            continue

        if stripped.startswith("- "):

            identifiers.append(
                stripped[2:].strip()
            )

    return identifiers


def _build_references(
    *,
    source: CanonicalIdentifier,
    identifiers: Iterable[str],
    relation: RelationType,
) -> list[Reference]:
    """
    Convert Canonical IDs into Reference objects.
    """

    references: list[Reference] = []

    for identifier in identifiers:

        target = CanonicalIdentifier.from_string(
            identifier
        )

        references.append(
            Reference(
                source=str(source),
                target=str(target),
                relation=relation,
            )
        )

    return references
