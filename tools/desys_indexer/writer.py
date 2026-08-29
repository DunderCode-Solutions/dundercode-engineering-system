"""Render and atomically write deterministic DESys index artifacts."""

from __future__ import annotations

import json
import os
from collections import defaultdict
from hashlib import sha256
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

import yaml

from tools.desys_indexer.config import SUPPORTED_ARTIFACTS
from tools.desys_indexer.models import IndexedDocument, RenderedIndexes
from tools.project_transaction import guard_operation

ARTIFACT_SCHEMA_VERSION = 1


def render_indexes(documents: list[IndexedDocument], artifacts: tuple[str, ...]) -> RenderedIndexes:
    """Render requested artifacts entirely in memory."""
    unsupported = sorted(set(artifacts) - set(SUPPORTED_ARTIFACTS))
    if unsupported:
        raise ValueError(f"Unsupported artifact(s): {', '.join(unsupported)}")

    ordered_documents = sorted(documents, key=lambda document: document.canonical_id)
    provisional_payloads = _build_payloads(ordered_documents, "")
    build_id = _build_id(provisional_payloads)
    payloads = _build_payloads(ordered_documents, build_id)
    files: dict[str, str] = {}
    for artifact in artifacts:
        payload = payloads[artifact]
        if artifact.endswith(".json"):
            files[artifact] = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
        else:
            files[artifact] = yaml.safe_dump(
                payload,
                sort_keys=False,
                allow_unicode=True,
                default_flow_style=False,
            )
    return RenderedIndexes(build_id=build_id, files=files)


def write_indexes(*, rendered: RenderedIndexes, output_dir: Path, verbose: bool = False) -> None:
    """Write all rendered artifacts using same-directory atomic replacements."""
    guard_operation(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    temporary_files: dict[str, Path] = {}
    try:
        for artifact, content in rendered.files.items():
            with NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=output_dir,
                prefix=f".{artifact}.",
                delete=False,
            ) as stream:
                stream.write(content)
                stream.flush()
                os.fsync(stream.fileno())
                temporary_files[artifact] = Path(stream.name)

        for artifact, temporary_path in temporary_files.items():
            destination = output_dir / artifact
            os.replace(temporary_path, destination)
            if verbose:
                print(f"[WRITE] {destination}")
    finally:
        for temporary_path in temporary_files.values():
            temporary_path.unlink(missing_ok=True)


def _build_id(payloads: dict[str, dict[str, Any]]) -> str:
    canonical_json = json.dumps(payloads, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return f"sha256:{sha256(canonical_json.encode('utf-8')).hexdigest()}"


def _build_payloads(documents: list[IndexedDocument], build_id: str) -> dict[str, dict[str, Any]]:
    aliases = _alias_map(documents)
    header = {"schema_version": ARTIFACT_SCHEMA_VERSION, "build_id": build_id}

    index_documents = [_index_entry(document) for document in documents]
    nodes = [_node_entry(document) for document in documents]
    edges = sorted(
        (
            {
                "source": document.canonical_id,
                "type": relationship["type"],
                "target": aliases.get(relationship["target"], relationship["target"]),
            }
            for document in documents
            for relationship in document.metadata.get("relationships", [])
        ),
        key=lambda edge: (edge["source"], edge["type"], edge["target"]),
    )

    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for document in documents:
        groups[document.path.parent.as_posix()].append(
            {
                "canonical_id": document.canonical_id,
                "document_id": document.document_id,
                "title": document.title,
                "path": document.path.as_posix(),
            }
        )
    navigation_groups = [
        {
            "path": path,
            "documents": sorted(entries, key=lambda entry: entry["canonical_id"]),
        }
        for path, entries in sorted(groups.items())
    ]

    search_documents = [_search_entry(document) for document in documents]
    return {
        "index.yaml": {**header, "document_count": len(documents), "documents": index_documents},
        "graph.yaml": {**header, "nodes": nodes, "edges": edges},
        "navigation.yaml": {**header, "groups": navigation_groups},
        "aliases.yaml": {**header, "aliases": aliases},
        "search-index.json": {**header, "documents": search_documents},
    }


def _index_entry(document: IndexedDocument) -> dict[str, Any]:
    metadata = document.metadata
    return {
        "metadata_schema": metadata["metadata_schema"],
        "document_id": document.document_id,
        "canonical_id": document.canonical_id,
        "title": document.title,
        "path": document.path.as_posix(),
        "node_type": metadata["node_type"],
        "document_class": metadata["document_class"],
        "version": metadata["version"],
        "status": metadata["status"],
        "language": metadata["language"],
        "owner": metadata["owner"],
        "domain": metadata.get("domain"),
        "discipline": metadata.get("discipline"),
        "architecture_model": metadata.get("architecture_model"),
        "authors": metadata.get("authors", []),
        "reviewers": metadata.get("reviewers", []),
        "applies_to": metadata.get("applies_to", []),
        "tags": metadata.get("tags", []),
        "aliases": sorted(metadata.get("aliases", [])),
        "legacy_status": metadata.get("legacy_status", False),
        "relationships": sorted(
            metadata.get("relationships", []),
            key=lambda relationship: (relationship["type"], relationship["target"]),
        ),
        "summary": document.summary,
    }


def _node_entry(document: IndexedDocument) -> dict[str, str]:
    return {
        "id": document.canonical_id,
        "document_id": document.document_id,
        "title": document.title,
        "node_type": document.metadata["node_type"],
        "path": document.path.as_posix(),
    }


def _search_entry(document: IndexedDocument) -> dict[str, Any]:
    return {
        "id": document.canonical_id,
        "document_id": document.document_id,
        "title": document.title,
        "path": document.path.as_posix(),
        "node_type": document.metadata["node_type"],
        "document_class": document.metadata["document_class"],
        "status": document.metadata["status"],
        "domain": document.metadata.get("domain"),
        "discipline": document.metadata.get("discipline"),
        "architecture_model": document.metadata.get("architecture_model"),
        "applies_to": document.metadata.get("applies_to", []),
        "tags": document.metadata.get("tags", []),
        "aliases": sorted(document.metadata.get("aliases", [])),
        "summary": document.summary,
        "content": document.body,
    }


def _alias_map(documents: list[IndexedDocument]) -> dict[str, str]:
    aliases = {
        alias: document.canonical_id
        for document in documents
        for alias in document.metadata.get("aliases", [])
    }
    return dict(sorted(aliases.items()))
