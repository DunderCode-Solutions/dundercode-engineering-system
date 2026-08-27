from __future__ import annotations

import json
from pathlib import Path, PurePosixPath

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
    validate_portable_target,
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


def test_inventory_schema_identity_matches_runtime_contract() -> None:
    schema = json.loads(Path("corpus/inventory.schema.json").read_text(encoding="utf-8"))

    assert schema["$id"] == "urn:uuid:8dfc7e36-1e0a-4b96-9f13-e98f8187a59a"
    assert schema["properties"]["inventory_schema"]["const"] == "1.2.0"
    assert schema["properties"]["release_tag"]["const"] == "v0.2.0-alpha.1"
    assert schema["properties"]["source_commit"]["const"] == "1ba18c126dc9adf035f64c0ca6eda75186e73b60"


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
  target: docs/desys/reference/knowledge/outside.json
  collection: knowledge
  classification: schema
  review_owner: DunderCode Engineering
""",
        encoding="utf-8",
    )

    with pytest.raises(InventoryError):
        load_asset_config(asset_config, config.repository_root, config.sources)


def test_explicit_legal_asset_can_use_managed_target(tmp_path: Path) -> None:
    config = _config(tmp_path)
    license_path = tmp_path / "LICENSE"
    license_path.write_text("License notice\n", encoding="utf-8")
    notice_path = tmp_path / "THIRD_PARTY_NOTICES.md"
    notice_path.write_text("Third-party notice\n", encoding="utf-8")
    asset_config = tmp_path / "assets.yaml"
    asset_config.write_text(
        """version: 1
assets:
- source: LICENSE
  target: docs/desys/LICENSE
  collection: legal
  classification: legal
  review_owner: DunderCode Engineering
- source: THIRD_PARTY_NOTICES.md
  target: docs/desys/THIRD_PARTY_NOTICES.md
  collection: legal
  classification: legal
  review_owner: DunderCode Engineering
""",
        encoding="utf-8",
    )

    assets = load_asset_config(asset_config, config.repository_root, config.sources)
    inventory = build_inventory(config, assets=assets)
    entry = inventory["entries"][0]

    assert entry["source"] == "LICENSE"
    assert entry["target"] == "docs/desys/LICENSE"
    assert entry["collection"] == "legal"
    assert entry["classification"] == "legal"


def test_asset_semantics_change_invalidates_approval(tmp_path: Path) -> None:
    config = _config(tmp_path)
    schema = config.sources[0] / "metadata.schema.json"
    schema.write_text('{"type": "object"}\n', encoding="utf-8")
    first_asset = CorpusAsset(
        schema,
        "schema",
        "DunderCode Engineering",
        PurePosixPath("docs/desys/reference/knowledge/metadata.schema.json"),
        "knowledge",
    )
    first = build_inventory(config, assets=(first_asset,))
    first["entries"][0]["distribution"] = "approved"
    changed_asset = CorpusAsset(
        schema,
        "supplemental",
        "DunderCode Engineering",
        PurePosixPath("docs/desys/reference/knowledge/renamed.schema.json"),
        "knowledge",
    )

    updated = build_inventory(config, previous=first, assets=(changed_asset,))

    assert updated["entries"][0]["distribution"] == "pending"
    assert updated["entries"][0]["review_fingerprint"] != first["entries"][0]["review_fingerprint"]


def test_inventory_rejects_changed_review_owner(tmp_path: Path) -> None:
    config = _config(tmp_path)
    readme = config.sources[0] / "README.md"
    readme.write_text("# Knowledge\n", encoding="utf-8")
    inventory = build_inventory(config)
    inventory["entries"][0]["review_owner"] = "Unreviewed Party"

    with pytest.raises(InventoryError, match="Review owner is stale"):
        validate_inventory(inventory, config)


@pytest.mark.parametrize(
    "target",
    (
        "docs/desys/reference/knowledge/CON.md",
        "docs/desys/reference/knowledge/bad:name.md",
        "docs/desys/reference/knowledge/bad\nname.md",
        "docs/desys/reference/knowledge/bad\x7fname.md",
    ),
)
def test_portable_target_rejects_cross_platform_names(target: str) -> None:
    with pytest.raises(InventoryError):
        validate_portable_target(PurePosixPath(target))


def test_asset_config_rejects_target_traversal(tmp_path: Path) -> None:
    config = _config(tmp_path)
    license_path = tmp_path / "LICENSE"
    license_path.write_text("License notice\n", encoding="utf-8")
    asset_config = tmp_path / "assets.yaml"
    asset_config.write_text(
        """version: 1
assets:
- source: LICENSE
  target: docs/desys/../outside
  collection: legal
  classification: legal
  review_owner: DunderCode Engineering
""",
        encoding="utf-8",
    )

    with pytest.raises(InventoryError):
        load_asset_config(asset_config, config.repository_root, config.sources)


def test_asset_config_rejects_windows_path_aliases(tmp_path: Path) -> None:
    config = _config(tmp_path)
    (tmp_path / "LICENSE").write_text("License notice\n", encoding="utf-8")
    asset_config = tmp_path / "assets.yaml"
    asset_config.write_text(
        """version: 1
assets:
- source: LICENSE
  target: docs/desys/..\\outside
  collection: legal
  classification: legal
  review_owner: DunderCode Engineering
""",
        encoding="utf-8",
    )

    with pytest.raises(InventoryError):
        load_asset_config(asset_config, config.repository_root, config.sources)


def test_asset_config_rejects_symlinked_source_ancestor(tmp_path: Path) -> None:
    config = _config(tmp_path)
    actual = config.sources[0] / "actual"
    actual.mkdir()
    (actual / "schema.json").write_text("{}\n", encoding="utf-8")
    (config.sources[0] / "linked").symlink_to(actual, target_is_directory=True)
    asset_config = tmp_path / "assets.yaml"
    asset_config.write_text(
        """version: 1
assets:
- source: knowledge/linked/schema.json
  target: docs/desys/reference/knowledge/linked/schema.json
  collection: knowledge
  classification: schema
  review_owner: DunderCode Engineering
""",
        encoding="utf-8",
    )

    with pytest.raises(InventoryError):
        load_asset_config(asset_config, config.repository_root, config.sources)


def test_asset_config_requires_legal_assets(tmp_path: Path) -> None:
    config = _config(tmp_path)
    asset_config = tmp_path / "assets.yaml"
    asset_config.write_text("version: 1\nassets: []\n", encoding="utf-8")

    with pytest.raises(InventoryError, match="Missing required legal asset"):
        load_asset_config(asset_config, config.repository_root, config.sources)
