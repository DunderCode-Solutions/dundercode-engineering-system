from __future__ import annotations

import hashlib
import os
from copy import deepcopy
from pathlib import Path, PurePosixPath

import pytest

from tools.build_corpus_bundle import BundleError, build_bundle, validate_or_write_bundle
from tools.build_corpus_inventory import load_asset_config, load_inventory, validate_inventory
from tools.desys_indexer.config import load_config


def _entry(root: Path, source: str, *, target: str | None = None, distribution: str = "approved") -> dict:
    path = root / source
    return {
        "source": source,
        "target": target or f"docs/desys/reference/{source}",
        "collection": "knowledge",
        "classification": "navigation",
        "distribution": distribution,
        "indexable": False,
        "checksum": f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}",
    }


def _indexable_entry(
    root: Path,
    source: str,
    document_id: str,
    canonical_id: str,
    metadata: str = "",
) -> dict:
    path = root / source
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"""---
document_id: {document_id}
canonical_id: {canonical_id}
{metadata}---

# Test
""",
        encoding="utf-8",
    )
    return {
        **_entry(root, source),
        "classification": "document",
        "indexable": True,
        "document_id": document_id,
        "canonical_id": canonical_id,
        "metadata_status": "draft",
    }


def _inventory(entries: list[dict]) -> dict:
    return {
        "inventory_schema": "1.2.0",
        "corpus_version": "0.1.0",
        "release_tag": "v0.2.0-alpha.1",
        "source_commit": "1ba18c126dc9adf035f64c0ca6eda75186e73b60",
        "entries": entries,
    }


def _tracked_inventory() -> tuple[dict, Path]:
    config = load_config(Path("tools/desys_indexer.yaml"))
    assets = load_asset_config(Path("corpus/assets.yaml"), config.repository_root, config.sources)
    inventory = load_inventory(Path("corpus/inventory.yaml"))
    assert inventory is not None
    validate_inventory(inventory, config, assets)
    return inventory, config.repository_root


def test_tracked_bundle_is_complete_and_current() -> None:
    inventory, repository_root = _tracked_inventory()
    manifest, files = build_bundle(inventory, repository_root)

    validate_or_write_bundle(repository_root / "tools/reference_corpus_data", files, check=True)

    approved = [entry for entry in inventory["entries"] if entry["distribution"] == "approved"]
    assert manifest["release_tag"] == inventory["release_tag"] == "v0.2.0-alpha.1"
    assert manifest["source_commit"] == inventory["source_commit"] == "1ba18c126dc9adf035f64c0ca6eda75186e73b60"
    assert len(manifest["entries"]) == len(approved) == 41
    assert {entry["source"] for entry in manifest["entries"]} == {entry["source"] for entry in approved}
    assert len(files) == 42


def test_bundle_rejects_link_to_non_approved_content() -> None:
    inventory, repository_root = _tracked_inventory()
    changed = deepcopy(inventory)
    schema = next(
        entry
        for entry in changed["entries"]
        if entry["source"] == "knowledge/architecture/metadata/desys-metadata.schema.json"
    )
    schema["distribution"] = "pending"

    with pytest.raises(BundleError, match="unavailable bundle content"):
        build_bundle(changed, repository_root)


def test_bundle_check_rejects_unexpected_resource(tmp_path: Path) -> None:
    inventory, repository_root = _tracked_inventory()
    _, files = build_bundle(inventory, repository_root)
    package_root = tmp_path / "reference_corpus_data"
    validate_or_write_bundle(package_root, files, check=False)
    (package_root / "unexpected.txt").write_text("unexpected\n", encoding="utf-8")

    with pytest.raises(BundleError, match="unexpected files"):
        validate_or_write_bundle(package_root, files, check=True)


@pytest.mark.parametrize(
    "unexpected",
    (
        PurePosixPath("files/docs/desys/reference/__init__.py"),
        PurePosixPath("files/docs/desys/reference/__pycache__/stale.pyc"),
    ),
)
def test_bundle_check_does_not_ignore_scaffolding_names_under_generated_files(
    tmp_path: Path,
    unexpected: PurePosixPath,
) -> None:
    files = {PurePosixPath("bundle.yaml"): b"bundle\n"}
    package_root = tmp_path / "reference_corpus_data"
    validate_or_write_bundle(package_root, files, check=False)
    stale = package_root / unexpected
    stale.parent.mkdir(parents=True, exist_ok=True)
    stale.write_bytes(b"unexpected\n")

    with pytest.raises(BundleError, match="unexpected files"):
        validate_or_write_bundle(package_root, files, check=True)


def test_bundle_check_rejects_empty_nested_pycache(tmp_path: Path) -> None:
    files = {PurePosixPath("bundle.yaml"): b"bundle\n"}
    package_root = tmp_path / "reference_corpus_data"
    validate_or_write_bundle(package_root, files, check=False)
    (package_root / "files/docs/desys/reference/__pycache__").mkdir(parents=True)

    with pytest.raises(BundleError, match="unexpected files"):
        validate_or_write_bundle(package_root, files, check=True)


def test_bundle_write_rejects_symlinked_files_root_before_external_deletion(tmp_path: Path) -> None:
    external = tmp_path / "external"
    victim = external / "nested/victim.txt"
    victim.parent.mkdir(parents=True)
    victim.write_text("consumer owned\n", encoding="utf-8")
    package_root = tmp_path / "reference_corpus_data"
    package_root.mkdir()
    (package_root / "files").symlink_to(external, target_is_directory=True)
    files = {
        PurePosixPath("bundle.yaml"): b"bundle\n",
        PurePosixPath("files/new.txt"): b"new\n",
    }

    with pytest.raises(BundleError, match="files root is a symlink"):
        validate_or_write_bundle(package_root, files, check=False)

    assert victim.read_text(encoding="utf-8") == "consumer owned\n"
    assert not (external / "new.txt").exists()
    assert not (package_root / "bundle.yaml").exists()


def test_bundle_rejects_symlinked_package_root(tmp_path: Path) -> None:
    external = tmp_path / "external"
    external.mkdir()
    package_root = tmp_path / "reference_corpus_data"
    package_root.symlink_to(external, target_is_directory=True)

    with pytest.raises(BundleError, match="package root is a symlink"):
        validate_or_write_bundle(package_root, {PurePosixPath("bundle.yaml"): b"bundle\n"}, check=True)


def test_bundle_preflights_legacy_and_current_roots_before_cleanup(tmp_path: Path) -> None:
    package_root = tmp_path / "reference_corpus_data"
    legacy = package_root / "files/stale.txt"
    legacy.parent.mkdir(parents=True)
    legacy.write_text("stale\n", encoding="utf-8")
    external = tmp_path / "external"
    external.mkdir()
    current = package_root / "corpus-files"
    current.mkdir()
    (current / "unsafe").symlink_to(external, target_is_directory=True)

    with pytest.raises(BundleError, match="contains a symlink"):
        validate_or_write_bundle(
            package_root,
            {PurePosixPath("bundle.yaml"): b"bundle\n"},
            check=False,
        )

    assert legacy.read_text(encoding="utf-8") == "stale\n"


@pytest.mark.parametrize("link_type", ("symlink", "hardlink"))
def test_bundle_preflights_descriptor_before_cleanup(tmp_path: Path, link_type: str) -> None:
    package_root = tmp_path / "reference_corpus_data"
    legacy = package_root / "files/stale.txt"
    legacy.parent.mkdir(parents=True)
    legacy.write_text("stale\n", encoding="utf-8")
    external = tmp_path / "external.yaml"
    external.write_text("consumer owned\n", encoding="utf-8")
    descriptor = package_root / "bundle.yaml"
    if link_type == "symlink":
        descriptor.symlink_to(external)
    else:
        os.link(external, descriptor)

    with pytest.raises(BundleError, match="bundle descriptor"):
        validate_or_write_bundle(
            package_root,
            {PurePosixPath("bundle.yaml"): b"bundle\n"},
            check=False,
        )

    assert external.read_text(encoding="utf-8") == "consumer owned\n"
    assert legacy.read_text(encoding="utf-8") == "stale\n"


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="FIFOs are not available on this platform")
def test_bundle_rejects_special_nodes_before_cleanup(tmp_path: Path) -> None:
    package_root = tmp_path / "reference_corpus_data"
    legacy = package_root / "files/stale.txt"
    legacy.parent.mkdir(parents=True)
    legacy.write_text("stale\n", encoding="utf-8")
    current = package_root / "corpus-files"
    current.mkdir()
    os.mkfifo(current / "unsafe")

    with pytest.raises(BundleError, match="special filesystem node"):
        validate_or_write_bundle(
            package_root,
            {PurePosixPath("bundle.yaml"): b"bundle\n"},
            check=False,
        )

    assert legacy.read_text(encoding="utf-8") == "stale\n"


def test_markdown_closure_handles_balanced_references_html_and_fenced_code(tmp_path: Path) -> None:
    source = tmp_path / "knowledge/source.md"
    source.parent.mkdir(parents=True)
    source.write_text(
        """[Balanced](target(with-parentheses).md)
[Apostrophe](owner's-target.md)
[Title](html-target.md "title with an unmatched ) character")
[Full reference][guide]
[Collapsed reference][]
[Shortcut]
<a href="html-target.md">HTML target</a>
<img src="image.bin">
[HTTPS](https://example.com/reference)
<a href="mailto:docs@example.com">Mail</a>

[guide]: reference-target.md
[collapsed reference]: collapsed-target.md
[shortcut]: shortcut-target.md

```markdown
[Unavailable example](not-approved.md)
<a href="also-not-approved.md">Example</a>
```
""",
        encoding="utf-8",
    )
    linked = (
        "target(with-parentheses).md",
        "owner's-target.md",
        "reference-target.md",
        "collapsed-target.md",
        "shortcut-target.md",
        "html-target.md",
        "image.bin",
    )
    for name in linked:
        (source.parent / name).write_text("linked\n", encoding="utf-8")
    entries = [_entry(tmp_path, "knowledge/source.md")]
    entries.extend(_entry(tmp_path, f"knowledge/{name}") for name in linked)

    manifest, files = build_bundle(_inventory(entries), tmp_path)

    assert len(manifest["entries"]) == len(entries)
    assert len(files) == len(entries) + 1


@pytest.mark.parametrize(
    ("body", "message"),
    (
        ("[Reference][missing]\n\n[missing]: pending.md\n", "unavailable bundle content"),
        ('<a href="pending.md">Pending</a>\n', "unavailable bundle content"),
        ("[File](file:///tmp/private.md)\n", "Unsupported Markdown link scheme"),
        ("[Drive](C:/private.md)\n", "Unsupported local Markdown link"),
        ("[Root](/private.md)\n", "Unsupported local Markdown link"),
        ("[Backslash](..\\private.md)\n", "Unsupported local Markdown link"),
    ),
)
def test_markdown_closure_rejects_unavailable_or_unsafe_destinations(
    tmp_path: Path,
    body: str,
    message: str,
) -> None:
    source = tmp_path / "knowledge/source.md"
    source.parent.mkdir(parents=True)
    source.write_text(body, encoding="utf-8")
    pending = source.parent / "pending.md"
    pending.write_text("pending\n", encoding="utf-8")
    entries = [
        _entry(tmp_path, "knowledge/source.md"),
        _entry(tmp_path, "knowledge/pending.md", distribution="pending"),
    ]

    with pytest.raises(BundleError, match=message):
        build_bundle(_inventory(entries), tmp_path)


def test_relationship_to_alias_owned_by_approved_document_is_available(tmp_path: Path) -> None:
    owner = _indexable_entry(
        tmp_path,
        "knowledge/owner.md",
        "RFC-0001",
        "rfc.test.owner",
        "aliases:\n- rfc.test.legacy-owner\n",
    )
    consumer = _indexable_entry(
        tmp_path,
        "knowledge/consumer.md",
        "RFC-0002",
        "rfc.test.consumer",
        "relationships:\n- type: references\n  target: rfc.test.legacy-owner\n",
    )

    manifest, _ = build_bundle(_inventory([consumer, owner]), tmp_path)

    assert len(manifest["entries"]) == 2


@pytest.mark.parametrize("identity", ("document", "canonical", "alias"))
def test_bundle_rejects_duplicate_approved_metadata_identities(tmp_path: Path, identity: str) -> None:
    first_document = "RFC-0001"
    second_document = first_document if identity == "document" else "RFC-0002"
    first_canonical = "rfc.test.first"
    second_canonical = first_canonical if identity == "canonical" else "rfc.test.second"
    alias_metadata = "aliases:\n- rfc.test.shared-alias\n" if identity == "alias" else ""
    first = _indexable_entry(
        tmp_path,
        "knowledge/first.md",
        first_document,
        first_canonical,
        alias_metadata,
    )
    second = _indexable_entry(
        tmp_path,
        "knowledge/second.md",
        second_document,
        second_canonical,
        alias_metadata,
    )

    with pytest.raises(BundleError, match=f"Duplicate approved {identity}"):
        build_bundle(_inventory([first, second]), tmp_path)


def test_bundle_rejects_alias_collision_with_approved_canonical_id(tmp_path: Path) -> None:
    first = _indexable_entry(tmp_path, "knowledge/first.md", "RFC-0001", "rfc.test.first")
    second = _indexable_entry(
        tmp_path,
        "knowledge/second.md",
        "RFC-0002",
        "rfc.test.second",
        "aliases:\n- rfc.test.first\n",
    )

    with pytest.raises(BundleError, match="alias collides with a canonical ID"):
        build_bundle(_inventory([first, second]), tmp_path)


def test_generated_bundle_files_are_not_executable() -> None:
    package_root = Path("tools/reference_corpus_data")

    assert all(path.stat().st_mode & 0o111 == 0 for path in package_root.rglob("*") if path.is_file())
