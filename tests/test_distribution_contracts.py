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
    load_reference_bundle,
    render_consumer_manifest,
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
        "compatibility-1.0.0.schema.json",
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
            package_version="0.2.0a1",
            package_source="dundercode-engineering-system==0.2.0a1",
        )
    )
    manifest_validator = Draft202012Validator(
        _json(CONTRACT_ROOT / "consumer-manifest-1.1.0.schema.json")
    )

    manifest_validator.validate(manifest)


def test_compatibility_matrix_matches_package_and_distribution_contracts() -> None:
    matrix = _yaml(Path("tools/reference_corpus_data/compatibility.yaml"))
    Draft202012Validator(
        _json(CONTRACT_ROOT / "compatibility-1.0.0.schema.json")
    ).validate(matrix)
    profile = load_compatibility_profile()
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))

    assert profile.package_version == version("dundercode-engineering-system")
    assert profile.package_version == pyproject["project"]["version"]
    assert profile.requires_python == metadata("dundercode-engineering-system")["Requires-Python"]
    assert set(profile.platforms) == {"linux", "macos", "windows"}
    assert profile.direct_predecessor_bundle_checksums == ()
    for field, relative in corpus_resources.CONTRACT_RESOURCES.items():
        content = (Path("tools/reference_corpus_data") / relative).read_bytes()
        assert profile.contract_checksums[field] == f"sha256:{hashlib.sha256(content).hexdigest()}"


def test_runtime_accepts_supported_manifest_fixture_and_rejects_unknown_versions() -> None:
    supported = (FIXTURE_ROOT / "consumer-manifest-1.1.0.yaml").read_bytes()
    unsupported = (FIXTURE_ROOT / "consumer-manifest-2.0.0.yaml").read_bytes()

    assert load_consumer_manifest(supported).package_version == "0.2.0a1"
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
        lambda: ("0.2.0a1", ">=3.13,<3.14"),
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
