#!/usr/bin/env python3
"""Validate structural and cross-artifact consistency of generated DESys indexes."""

from __future__ import annotations

import argparse
import json
import re
import sys
from copy import deepcopy
from hashlib import sha256
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.desys_indexer.config import SUPPORTED_ARTIFACTS, load_config
from tools.desys_metadata import UniqueKeyLoader, managed_documents
from tools.project_transaction import TransactionError, guard_operation

BUILD_ID_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("skills/generated"),
        help="Generated artifact directory.",
    )
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    try:
        summary = validate_generated_artifacts(arguments.output)
    except (OSError, ValueError, json.JSONDecodeError, yaml.YAMLError, TransactionError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        f"Validated {summary['artifact_count']} artifacts for "
        f"{summary['document_count']} documents ({summary['build_id']})."
    )
    return 0


def validate_generated_artifacts(output: Path) -> dict[str, Any]:
    """Validate generated files and return a compact summary."""
    guard_operation(output)
    output = output.resolve()
    _require(output.is_dir(), f"Artifact directory does not exist: {output}")

    files = {path.name for path in output.iterdir() if path.is_file()}
    _require(files == set(SUPPORTED_ARTIFACTS), f"Unexpected artifact set: {sorted(files)}")
    payloads = {
        name: _load_artifact(output / name)
        for name in SUPPORTED_ARTIFACTS
    }

    build_ids = {payload.get("build_id") for payload in payloads.values()}
    _require(len(build_ids) == 1, "Artifacts have different build IDs.")
    build_id = build_ids.pop()
    _require(
        isinstance(build_id, str) and BUILD_ID_PATTERN.fullmatch(build_id) is not None,
        "Invalid build ID.",
    )
    _require(
        all(payload.get("schema_version") == 1 for payload in payloads.values()),
        "Unsupported artifact schema version.",
    )

    index_payload = payloads["index.yaml"]
    documents = index_payload.get("documents")
    _require(isinstance(documents, list), "index.yaml documents must be a list.")
    canonical_ids = [document["canonical_id"] for document in documents]
    _require(canonical_ids == sorted(canonical_ids), "Index documents are not sorted.")
    _require(len(canonical_ids) == len(set(canonical_ids)), "Index contains duplicate canonical IDs.")
    _require(index_payload.get("document_count") == len(documents), "index.yaml document_count is inconsistent.")

    repository_root = output.parents[1]
    for document in documents:
        path_value = document["path"]
        relative_path = PurePosixPath(path_value)
        _require(not relative_path.is_absolute(), f"Absolute document path: {path_value}")
        _require(".." not in relative_path.parts and "\\" not in path_value, f"Unsafe document path: {path_value}")
        _require((repository_root / path_value).is_file(), f"Indexed document does not exist: {path_value}")

    index_identity = {
        document["canonical_id"]: (
            document["document_id"],
            document["title"],
            document["path"],
            document["node_type"],
        )
        for document in documents
    }
    config = load_config(repository_root / "tools/desys_indexer.yaml")
    discovered_paths = {
        path.relative_to(repository_root).as_posix()
        for path in managed_documents(
            repository_root,
            sources=config.sources,
            is_excluded=config.is_excluded,
        )
        if path.read_text(encoding="utf-8").strip()
    }
    indexed_paths = {document["path"] for document in documents}
    _require(indexed_paths == discovered_paths, "Generated index coverage differs from the configured corpus.")

    _validate_graph(payloads["graph.yaml"], canonical_ids, index_identity)
    _validate_navigation(payloads["navigation.yaml"], canonical_ids)
    _validate_aliases(payloads["aliases.yaml"], canonical_ids)

    search_documents = payloads["search-index.json"].get("documents")
    _require(isinstance(search_documents, list), "Search documents must be a list.")
    _require(
        [document["id"] for document in search_documents] == canonical_ids,
        "Search index differs from canonical index.",
    )

    provisional = deepcopy(payloads)
    for payload in provisional.values():
        payload["build_id"] = ""
    canonical_json = json.dumps(provisional, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    expected_build_id = f"sha256:{sha256(canonical_json.encode('utf-8')).hexdigest()}"
    _require(build_id == expected_build_id, "Build ID does not match artifact content.")

    return {
        "artifact_count": len(payloads),
        "document_count": len(documents),
        "build_id": build_id,
    }


def _load_artifact(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    payload = (
        json.loads(text)
        if path.suffix == ".json"
        else yaml.load(text, Loader=UniqueKeyLoader)
    )
    _require(isinstance(payload, dict), f"{path}: root must be a mapping.")
    return payload


def _validate_graph(
    graph: dict[str, Any],
    canonical_ids: list[str],
    index_identity: dict[str, tuple[str, str, str, str]],
) -> None:
    nodes = graph.get("nodes")
    edges = graph.get("edges")
    _require(isinstance(nodes, list) and isinstance(edges, list), "Graph nodes and edges must be lists.")
    _require([node["id"] for node in nodes] == canonical_ids, "Graph nodes differ from index documents.")
    graph_identity = {
        node["id"]: (node["document_id"], node["title"], node["path"], node["node_type"])
        for node in nodes
    }
    _require(graph_identity == index_identity, "Graph identities are inconsistent.")
    edge_order = [(edge["source"], edge["type"], edge["target"]) for edge in edges]
    _require(edge_order == sorted(edge_order), "Graph edges are not sorted.")
    _require(
        all(edge["source"] in index_identity and edge["target"] in index_identity for edge in edges),
        "Graph contains an unresolved edge.",
    )


def _validate_navigation(navigation: dict[str, Any], canonical_ids: list[str]) -> None:
    groups = navigation.get("groups")
    _require(isinstance(groups, list), "Navigation groups must be a list.")
    group_paths = [group["path"] for group in groups]
    _require(group_paths == sorted(group_paths), "Navigation groups are not sorted.")
    navigation_ids = [
        document["canonical_id"]
        for group in groups
        for document in group["documents"]
    ]
    _require(len(navigation_ids) == len(set(navigation_ids)), "Navigation contains duplicate documents.")
    _require(set(navigation_ids) == set(canonical_ids), "Navigation coverage is incomplete.")


def _validate_aliases(aliases_payload: dict[str, Any], canonical_ids: list[str]) -> None:
    aliases = aliases_payload.get("aliases")
    _require(isinstance(aliases, dict), "Aliases must be a mapping.")
    _require(list(aliases) == sorted(aliases), "Aliases are not sorted.")
    _require(not set(aliases) & set(canonical_ids), "Alias conflicts with a canonical ID.")
    _require(all(target in canonical_ids for target in aliases.values()), "Alias target does not resolve.")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


if __name__ == "__main__":
    raise SystemExit(main())
