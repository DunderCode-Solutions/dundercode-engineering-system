from __future__ import annotations

import hashlib
import json
import shutil
import tomllib
from importlib.metadata import metadata, version
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator

from tools import corpus_resources
from tools.corpus_resources import (
    CorpusResourceError,
    UnsupportedCorpusBundleError,
    load_compatibility_profile,
    load_consumer_manifest,
    load_predecessor_descriptor,
    load_reference_bundle,
    render_consumer_manifest,
    validate_predecessor_manifest,
)

CONTRACT_ROOT = Path("tools/reference_corpus_data/contracts")
FIXTURE_ROOT = Path("tests/fixtures/contracts")


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    "name",
    (
        "reference-bundle-1.1.0.schema.json",
        "consumer-manifest-1.1.0.schema.json",
        "compatibility-1.1.0.schema.json",
        "predecessor-descriptor-1.0.0.schema.json",
    ),
)
def test_distribution_contract_is_a_valid_draft_2020_12_schema(name: str) -> None:
    Draft202012Validator.check_schema(_json(CONTRACT_ROOT / name))


@pytest.mark.parametrize(
    ("schema_name", "supported_name", "unsupported_name", "version_field"),
    (
        (
            "reference-bundle-1.1.0.schema.json",
            "reference-bundle-1.1.0.yaml",
            "reference-bundle-2.0.0.yaml",
            "bundle_schema",
        ),
        (
            "consumer-manifest-1.1.0.schema.json",
            "consumer-manifest-1.1.0.yaml",
            "consumer-manifest-2.0.0.yaml",
            "manifest_schema",
        ),
    ),
)
def test_contract_fixtures_accept_supported_and_reject_unknown_major_versions(
    schema_name: str,
    supported_name: str,
    unsupported_name: str,
    version_field: str,
) -> None:
    validator = Draft202012Validator(_json(CONTRACT_ROOT / schema_name))

    assert not list(validator.iter_errors(_yaml(FIXTURE_ROOT / supported_name)))
    errors = list(validator.iter_errors(_yaml(FIXTURE_ROOT / unsupported_name)))

    assert any(list(error.path) == [version_field] for error in errors)


def test_tracked_bundle_and_rendered_manifest_match_formal_contracts() -> None:
    bundle_payload = _yaml(Path("tools/reference_corpus_data/bundle.yaml"))
    bundle_validator = Draft202012Validator(
        _json(CONTRACT_ROOT / "reference-bundle-1.1.0.schema.json")
    )
    bundle_validator.validate(bundle_payload)
    bundle = load_reference_bundle()
    manifest = yaml.safe_load(
        render_consumer_manifest(
            bundle,
            package_name="dundercode-engineering-system",
            package_version="0.3.0a1",
            package_source="dundercode-engineering-system==0.3.0a1",
        )
    )
    manifest_validator = Draft202012Validator(
        _json(CONTRACT_ROOT / "consumer-manifest-1.1.0.schema.json")
    )

    manifest_validator.validate(manifest)


def test_compatibility_matrix_matches_package_and_distribution_contracts() -> None:
    matrix = _yaml(Path("tools/reference_corpus_data/compatibility.yaml"))
    Draft202012Validator(
        _json(CONTRACT_ROOT / "compatibility-1.1.0.schema.json")
    ).validate(matrix)
    profile = load_compatibility_profile()
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))

    assert profile.package_version == version("dundercode-engineering-system")
    assert profile.package_version == pyproject["project"]["version"]
    assert profile.requires_python == metadata("dundercode-engineering-system")["Requires-Python"]
    assert set(profile.platforms) == {"linux", "macos"}
    assert profile.direct_predecessor_bundle_checksums == (
        "sha256:d78bb3a685bf285f29d542d1709be9874842f759f00d9739ba073ce94633f62a",
    )
    for field, relative in corpus_resources.CONTRACT_RESOURCES.items():
        content = (Path("tools/reference_corpus_data") / relative).read_bytes()
        assert profile.contract_checksums[field] == f"sha256:{hashlib.sha256(content).hexdigest()}"


def test_runtime_accepts_supported_manifest_fixture_and_rejects_unknown_versions() -> None:
    bundle = load_reference_bundle()
    supported = render_consumer_manifest(
        bundle,
        package_name="dundercode-engineering-system",
        package_version="0.3.0a1",
        package_source="dundercode-engineering-system==0.3.0a1",
    )
    unsupported = (FIXTURE_ROOT / "consumer-manifest-2.0.0.yaml").read_bytes()

    assert load_consumer_manifest(supported).package_version == "0.3.0a1"
    with pytest.raises(CorpusResourceError, match="Unsupported consumer manifest schema"):
        load_consumer_manifest(unsupported)
    with pytest.raises(UnsupportedCorpusBundleError, match="No compatibility profile"):
        load_compatibility_profile("9.0.0")


def test_runtime_rejects_unknown_bundle_schema_fixture(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    source = Path("tools/reference_corpus_data")
    package = tmp_path / "reference_corpus_data"
    shutil.copytree(source, package)
    shutil.copyfile(FIXTURE_ROOT / "reference-bundle-2.0.0.yaml", package / "bundle.yaml")
    monkeypatch.setattr(corpus_resources.resources, "files", lambda _: package)

    with pytest.raises(CorpusResourceError, match="Unsupported corpus bundle schema"):
        load_reference_bundle()


def test_runtime_rejects_package_python_mismatch(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        corpus_resources,
        "_installed_package_contract",
        lambda: ("0.3.0a1", ">=3.13,<3.14"),
    )

    with pytest.raises(CorpusResourceError, match="requires_python does not match"):
        load_reference_bundle()


def test_runtime_rejects_tampered_packaged_contract(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    source = Path("tools/reference_corpus_data")
    package = tmp_path / "reference_corpus_data"
    shutil.copytree(source, package)
    contract = package / "contracts/reference-bundle-1.1.0.schema.json"
    contract.write_bytes(contract.read_bytes() + b"\n")
    monkeypatch.setattr(corpus_resources.resources, "files", lambda _: package)

    with pytest.raises(CorpusResourceError, match="Packaged contract checksum mismatch"):
        load_reference_bundle()


def _predecessor_manifest_payload() -> dict:
    descriptor = load_predecessor_descriptor(
        "sha256:d78bb3a685bf285f29d542d1709be9874842f759f00d9739ba073ce94633f62a"
    )
    return {
        "manifest_schema": "1.1.0",
        "package_name": "dundercode-engineering-system",
        "package_version": descriptor.predecessor_package_version,
        "package_source": "dundercode-engineering-system==0.2.0a1",
        "release_tag": descriptor.release_tag,
        "source_commit": descriptor.source_commit,
        "corpus_version": descriptor.corpus_version,
        "bundle_checksum": descriptor.bundle_checksum,
        "entries": [
            {
                "source": entry.source,
                "target": entry.target.as_posix(),
                "collection": entry.collection,
                "classification": entry.classification,
                "distribution": "approved",
                "original_checksum": entry.checksum,
                "installed_checksum": entry.checksum,
                **({"document_id": entry.document_id} if entry.document_id is not None else {}),
                **({"canonical_id": entry.canonical_id} if entry.canonical_id is not None else {}),
            }
            for entry in descriptor.entries
        ],
    }


def test_packaged_predecessor_descriptor_is_complete_and_matches_contract() -> None:
    path = Path(
        "tools/reference_corpus_data/predecessors/"
        "sha256-d78bb3a685bf285f29d542d1709be9874842f759f00d9739ba073ce94633f62a.yaml"
    )
    payload = _yaml(path)
    validator = Draft202012Validator(
        _json(CONTRACT_ROOT / "predecessor-descriptor-1.0.0.schema.json")
    )
    validator.validate(payload)
    unsupported = {**payload, "predecessor_descriptor_schema": "2.0.0"}
    assert any(
        list(error.path) == ["predecessor_descriptor_schema"]
        for error in validator.iter_errors(unsupported)
    )
    descriptor = load_predecessor_descriptor(payload["bundle_checksum"])

    assert descriptor.target_bundle_checksum == load_reference_bundle().bundle_checksum
    assert descriptor.accepted_manifest_schemas == ("1.1.0",)
    assert len(descriptor.entries) == 41


def test_exact_v02_predecessor_manifest_is_trusted_before_planning() -> None:
    content = yaml.safe_dump(_predecessor_manifest_payload(), sort_keys=False).encode("utf-8")

    manifest, descriptor = validate_predecessor_manifest(content)

    assert manifest.bundle_checksum == descriptor.bundle_checksum
    assert manifest.package_version == "0.2.0a1"


@pytest.mark.parametrize(
    ("mutate", "message"),
    (
        (lambda value: value.update(release_tag="v0.2.0-alpha.2"), "release_tag does not match"),
        (lambda value: value.update(source_commit="f" * 40), "provenance does not match"),
        (
            lambda value: value["entries"][0].update(original_checksum=f"sha256:{'f' * 64}"),
            "entries do not match",
        ),
    ),
)
def test_forged_predecessor_manifest_fails_closed(mutate, message: str) -> None:
    payload = _predecessor_manifest_payload()
    mutate(payload)

    with pytest.raises(CorpusResourceError, match=message):
        validate_predecessor_manifest(yaml.safe_dump(payload, sort_keys=False).encode("utf-8"))


def test_unknown_predecessor_snapshot_is_not_trusted() -> None:
    payload = _predecessor_manifest_payload()
    payload["bundle_checksum"] = f"sha256:{'f' * 64}"

    with pytest.raises(UnsupportedCorpusBundleError, match="declared direct predecessor"):
        validate_predecessor_manifest(yaml.safe_dump(payload, sort_keys=False).encode("utf-8"))


def test_tampered_predecessor_descriptor_is_rejected_before_parsing(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    source = Path("tools/reference_corpus_data")
    package = tmp_path / "reference_corpus_data"
    shutil.copytree(source, package)
    descriptor = package / (
        "predecessors/sha256-d78bb3a685bf285f29d542d1709be9874842f759f00d9739ba073ce94633f62a.yaml"
    )
    descriptor.write_bytes(descriptor.read_bytes() + b"\n")
    monkeypatch.setattr(corpus_resources.resources, "files", lambda _: package)

    with pytest.raises(CorpusResourceError, match="descriptor checksum mismatch"):
        load_reference_bundle()
