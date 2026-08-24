from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from tools.build_corpus_inventory import (
    CorpusAsset,
    InventoryError,
    build_inventory,
    load_asset_config,
    load_inventory,
    render_inventory,
    validate_inventory,
)
from tools.desys_indexer.config import IndexerConfig, load_config


def _config(root: Path) -> IndexerConfig:
    source = root / "knowledge"
    source.mkdir()
    return IndexerConfig(
        version=1,
        repository_root=root,
        sources=(source,),
        output_directory=root / "generated",
        exclude=(),
        artifacts=("index.yaml",),
    )


def _write_document(path: Path, body: str = "Body.\n") -> None:
    path.write_text(
        """---
metadata_schema: 1.0.0
document_id: RFC-0001
canonical_id: rfc.test.inventory
title: Inventory Test
node_type: proposal
document_class: informative
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
---

# RFC-0001 - Inventory Test

"""
        + body,
        encoding="utf-8",
    )


def test_tracked_inventory_is_complete_and_current() -> None:
    config = load_config(Path("tools/desys_indexer.yaml"))
    assets = load_asset_config(Path("corpus/assets.yaml"), config.repository_root, config.sources)
    inventory = load_inventory(Path("corpus/inventory.yaml"))

    assert inventory is not None
    validate_inventory(inventory, config, assets)
    assert render_inventory(build_inventory(config, inventory, assets)) == Path("corpus/inventory.yaml").read_text(
        encoding="utf-8"
    )


def test_changed_approved_document_returns_to_pending(tmp_path: Path) -> None:
    config = _config(tmp_path)
    document = config.sources[0] / "RFC-0001-inventory-test.md"
    _write_document(document)
    first = build_inventory(config)
    first["entries"][0]["distribution"] = "approved"

    unchanged = build_inventory(config, first)
    assert unchanged["entries"][0]["distribution"] == "approved"

    _write_document(document, "Changed body.\n")
    changed = build_inventory(config, unchanged)
    assert changed["entries"][0]["distribution"] == "pending"


def test_empty_managed_document_is_excluded(tmp_path: Path) -> None:
    config = _config(tmp_path)
    (config.sources[0] / "RFC-0001-empty.md").write_text("", encoding="utf-8")

    inventory = build_inventory(config)
    entry = inventory["entries"][0]

    assert entry["classification"] == "placeholder"
    assert entry["distribution"] == "excluded"
    assert entry["exclusion_reason"] == "empty-placeholder"
    assert yaml.safe_load(render_inventory(inventory)) == inventory


def test_empty_unmanaged_document_is_excluded(tmp_path: Path) -> None:
    config = _config(tmp_path)
    (config.sources[0] / "README.md").write_text("", encoding="utf-8")

    inventory = build_inventory(config)
    entry = inventory["entries"][0]

    assert entry["classification"] == "navigation"
    assert entry["distribution"] == "excluded"
    assert entry["exclusion_reason"] == "empty-file"


def test_explicit_non_markdown_asset_is_inventoried(tmp_path: Path) -> None:
    config = _config(tmp_path)
    schema = config.sources[0] / "metadata.schema.json"
    schema.write_text('{"type": "object"}\n', encoding="utf-8")
    assets = (CorpusAsset(schema, "schema", "DunderCode Engineering"),)

    inventory = build_inventory(config, assets=assets)
    entry = inventory["entries"][0]

    assert entry["source"] == "knowledge/metadata.schema.json"
    assert entry["target"] == "docs/desys/reference/knowledge/metadata.schema.json"
    assert entry["classification"] == "schema"
    assert entry["distribution"] == "pending"
    assert entry["indexable"] is False


def test_asset_config_rejects_path_traversal(tmp_path: Path) -> None:
    config = _config(tmp_path)
    asset_config = tmp_path / "assets.yaml"
    asset_config.write_text(
        """version: 1
assets:
- source: ../outside.json
  classification: schema
  review_owner: DunderCode Engineering
""",
        encoding="utf-8",
    )

    with pytest.raises(InventoryError):
        load_asset_config(asset_config, config.repository_root, config.sources)
