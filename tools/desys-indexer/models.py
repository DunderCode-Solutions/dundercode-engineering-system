"""
DESys Indexer Domain Models

Core domain models shared across the DESys Indexer.

Author:
    DunderCode Engineering
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from uuid import UUID, uuid4


# =============================================================================
# Enumerations
# =============================================================================


class ArtifactType(str, Enum):
    """Generated artifact types."""

    INDEX = "index.yaml"
    GRAPH = "graph.yaml"
    NAVIGATION = "navigation.yaml"
    ALIASES = "aliases.yaml"
    SEARCH_INDEX = "search-index.json"


class LibraryType(str, Enum):
    """Supported DESys libraries."""

    DES = "DES"
    DAR = "DAR"

    DEP = "DEP"
    DEA = "DEA"
    DET = "DET"

    DSK = "DSK"
    DSP = "DSP"

    UNKNOWN = "UNKNOWN"


class RelationType(str, Enum):
    """Relationship between documents."""

    PARENT = "parent"

    CHILD = "child"

    RELATED = "related"

    DEPENDS_ON = "depends_on"

    REFERENCES = "references"


# =============================================================================
# Metadata
# =============================================================================

@dataclass(slots=True, frozen=True)
class CanonicalIdentifier:
    """
    Canonical identifier used across DESys.

    Example:

        des.ai.prompt-engineering
    """

    raw: str

    library: str

    domain: str

    slug: str

    @classmethod
    def from_string(
        cls,
        canonical_id: str,
    ) -> "CanonicalIdentifier":

        parts = canonical_id.split(".")

        if len(parts) < 3:
            raise ValueError(
                f"Invalid Canonical ID: {canonical_id}"
            )

        return cls(
            raw=canonical_id,
            library=parts[0],
            domain=parts[1],
            slug=".".join(parts[2:]),
        )

    def __str__(self) -> str:
        return self.raw


@dataclass(slots=True, frozen=True)
class DocumentMetadata:
    """
    Metadata extracted from a DESys Markdown document.
    """

    document_number: str

    canonical_id: CanonicalIdentifier

    document_class: str

    version: str

    status: str

    canonical_language: str

    owner: str

    @property
    def document_number(self) -> str:
        return self.metadata.document_number


    @property
    def canonical_id(self) -> CanonicalIdentifier:
        return self.metadata.canonical_id


    @property
    def library(self) -> str:
        return self.canonical_id.library


    @property
    def domain(self) -> str:
        return self.canonical_id.domain


    @property
    def slug(self) -> str:
        return self.canonical_id.slug

    def as_dict(self) -> dict[str, str]:

        return {
            "document_number": self.document_number,
            "canonical_id": str(self.canonical_id),
            "document_class": self.document_class,
            "version": self.version,
            "status": self.status,
            "canonical_language": self.canonical_language,
            "owner": self.owner,
        }


# =============================================================================
# References
# =============================================================================


@dataclass(slots=True, frozen=True)
class Reference:
    """
    Relationship between two documents.
    """

    source: str

    target: str

    relation: RelationType = RelationType.RELATED


# =============================================================================
# Documents
# =============================================================================


@dataclass(slots=True)
class Document:
    """
    DESys Markdown document.
    """

    uuid: UUID = field(default_factory=uuid4)

    library: LibraryType = LibraryType.UNKNOWN

    path: Path = Path()

    title: str = ""

    metadata: DocumentMetadata | None = None

    summary: str | None = None

    headings: list[str] = field(default_factory=list)

    tags: list[str] = field(default_factory=list)

    aliases: list[str] = field(default_factory=list)

    references: list[Reference] = field(default_factory=list)

    # -------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------

    @property
    def canonical_id(self) -> str:
        """Returns the canonical document identifier."""
        if self.metadata is None:
            return ""
        return self.metadata.canonical_id

    @property
    def filename(self) -> str:
        """Returns the filename."""
        return self.path.name

    @property
    def stem(self) -> str:
        """Returns the filename without extension."""
        return self.path.stem

    @property
    def library_name(self) -> str:
        """Returns the library name."""
        return self.library.value

    # -------------------------------------------------------------------------
    # Mutators
    # -------------------------------------------------------------------------

    def add_heading(self, heading: str) -> None:
        """Adds a heading."""
        if heading not in self.headings:
            self.headings.append(heading)

    def add_tag(self, tag: str) -> None:
        """Adds a tag."""
        if tag not in self.tags:
            self.tags.append(tag)

    def add_alias(self, alias: str) -> None:
        """Adds an alias."""
        if alias not in self.aliases:
            self.aliases.append(alias)

    def add_reference(self, reference: Reference) -> None:
        """Adds a cross-reference."""
        self.references.append(reference)


# =============================================================================
# Libraries
# =============================================================================


@dataclass(slots=True)
class Library:
    """
    DESys documentation library.
    """

    name: LibraryType

    path: Path

    documents: list[Document] = field(default_factory=list)

    def add_document(self, document: Document) -> None:
        """Adds a document to the library."""
        self.documents.append(document)

    @property
    def count(self) -> int:
        """Returns the number of indexed documents."""
        return len(self.documents)

    @property
    def canonical_name(self) -> str:
        """Returns the canonical library name."""
        return self.name.value