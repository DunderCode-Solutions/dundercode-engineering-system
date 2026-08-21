"""Immutable models shared by the DESys indexing pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Any


@dataclass(frozen=True, slots=True)
class IndexedDocument:
    path: PurePosixPath
    metadata: dict[str, Any]
    body: str
    headings: tuple[str, ...]
    summary: str | None

    @property
    def document_id(self) -> str:
        return self.metadata["document_id"]

    @property
    def canonical_id(self) -> str:
        return self.metadata["canonical_id"]

    @property
    def title(self) -> str:
        return self.metadata["title"]

    @property
    def library(self) -> str:
        return self.canonical_id.split(".", 1)[0]

    @property
    def domain(self) -> str:
        return self.canonical_id.split(".", 2)[1]


@dataclass(frozen=True, slots=True)
class RenderedIndexes:
    build_id: str
    files: dict[str, str]
