from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
import yaml

from tools import corpus_resources
from tools.corpus_resources import (
    CorpusResourceError,
    load_consumer_manifest,
    load_reference_bundle,
    validate_target,
)


def test_packaged_resources_match_all_bundle_checksums() -> None:
    bundle = load_reference_bundle()

    assert bundle.bundle_schema == "1.0.0"
    assert bundle.corpus_version == "0.1.0"
    assert len(bundle.entries) == 41
    assert {path.as_posix() for path in bundle.source_roots} == {
        "docs/desys/reference/delivery",
        "docs/desys/reference/engineering",
        "docs/desys/reference/foundation",
        "docs/desys/reference/knowledge",
    }
    for entry in bundle.entries:
        assert f"sha256:{hashlib.sha256(entry.content).hexdigest()}" == entry.checksum


def test_resource_loader_rejects_duplicate_yaml_keys(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    package = tmp_path / "reference_corpus_data"
    package.mkdir()
    (package / "bundle.yaml").write_text(
        "bundle_schema: 1.0.0\nbundle_schema: 1.0.0\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(corpus_resources.resources, "files", lambda _: package)

    with pytest.raises(CorpusResourceError, match="duplicate key"):
        load_reference_bundle()


def test_resource_loader_rejects_unchecked_target_paths(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    tracked = Path("tools/reference_corpus_data/bundle.yaml").read_text(encoding="utf-8")
    data = yaml.safe_load(tracked)
    data["entries"][0]["target"] = "../outside"
    descriptor = {key: data[key] for key in ("bundle_schema", "inventory_schema", "corpus_version", "entries")}
    descriptor_bytes = yaml.safe_dump(
        descriptor, sort_keys=False, allow_unicode=False, width=120
    ).encode("utf-8")
    data["bundle_checksum"] = f"sha256:{hashlib.sha256(descriptor_bytes).hexdigest()}"
    package = tmp_path / "reference_corpus_data"
    package.mkdir()
    (package / "bundle.yaml").write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    monkeypatch.setattr(corpus_resources.resources, "files", lambda _: package)

    with pytest.raises(CorpusResourceError, match="safe relative path"):
        load_reference_bundle()


@pytest.mark.parametrize(
    "target",
    [
        "docs/desys/reference/con/CON.txt",
        "docs/desys/reference/name./file.md",
        "docs/desys/reference/name /file.md",
        "docs/desys/reference/knowledge/stream:secret",
        "docs/desys/reference/knowledge/control\x7f.md",
    ],
)
def test_runtime_target_validation_rejects_platform_aliases(target: str) -> None:
    with pytest.raises(CorpusResourceError, match="not portable"):
        validate_target(target)


def test_consumer_manifest_rejects_casefold_equivalent_paths() -> None:
    entry = {
        "source": "knowledge/A.md",
        "target": "docs/desys/reference/knowledge/A.md",
        "collection": "knowledge",
        "classification": "navigation",
        "distribution": "approved",
        "original_checksum": f"sha256:{'a' * 64}",
        "installed_checksum": f"sha256:{'a' * 64}",
    }
    payload = {
        "manifest_schema": "1.0.0",
        "package_name": "dundercode-engineering-system",
        "package_version": "0.1.0a1",
        "package_source": "dundercode-engineering-system==0.1.0a1",
        "corpus_version": "0.1.0",
        "bundle_checksum": f"sha256:{'b' * 64}",
        "entries": [entry, {**entry, "source": "knowledge/a.md", "target": "docs/desys/reference/knowledge/a.md"}],
    }

    with pytest.raises(CorpusResourceError, match="supported filesystems"):
        load_consumer_manifest(yaml.safe_dump(payload).encode("utf-8"))


def test_consumer_manifest_rejects_nested_nonstring_keys() -> None:
    payload = {
        "manifest_schema": "1.0.0",
        "package_name": "dundercode-engineering-system",
        "package_version": "0.1.0a1",
        "package_source": "dundercode-engineering-system==0.1.0a1",
        "corpus_version": "0.1.0",
        "bundle_checksum": f"sha256:{'b' * 64}",
        "entries": [
            {
                "source": "knowledge/a.md",
                "target": "docs/desys/reference/knowledge/a.md",
                "collection": "knowledge",
                "classification": "navigation",
                "distribution": "approved",
                "original_checksum": f"sha256:{'a' * 64}",
                "installed_checksum": f"sha256:{'a' * 64}",
                1: "unexpected",
            }
        ],
    }

    with pytest.raises(CorpusResourceError, match="string field names"):
        load_consumer_manifest(yaml.safe_dump(payload).encode("utf-8"))


def test_resource_loader_rejects_filesystem_symlinks(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    package = tmp_path / "reference_corpus_data"
    package.mkdir()
    external = tmp_path / "external"
    external.mkdir()
    entries = []
    for name, content in (("LICENSE", b"license\n"), ("THIRD_PARTY_NOTICES.md", b"notices\n")):
        source = external / name
        source.write_bytes(content)
        target = f"docs/desys/{name}"
        destination = package / "corpus-files" / target
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.symlink_to(source)
        entries.append(
            {
                "source": name,
                "target": target,
                "collection": "legal",
                "classification": "legal",
                "indexable": False,
                "checksum": f"sha256:{hashlib.sha256(content).hexdigest()}",
            }
        )
    descriptor = {
        "bundle_schema": "1.0.0",
        "inventory_schema": "1.1.0",
        "corpus_version": "0.1.0",
        "entries": entries,
    }
    descriptor_bytes = yaml.safe_dump(descriptor, sort_keys=False, allow_unicode=False, width=120).encode("utf-8")
    manifest = {**descriptor, "bundle_checksum": f"sha256:{hashlib.sha256(descriptor_bytes).hexdigest()}"}
    (package / "bundle.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    monkeypatch.setattr(corpus_resources.resources, "files", lambda _: package)

    with pytest.raises(CorpusResourceError, match="symlink"):
        load_reference_bundle()
