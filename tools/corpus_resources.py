"""Load and validate the immutable reference corpus package resources."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from dataclasses import dataclass
from importlib import resources
from importlib.metadata import PackageNotFoundError, metadata, version
from importlib.resources.abc import Traversable
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

from tools.build_corpus_inventory import InventoryError, validate_portable_target
from tools.desys_metadata import UniqueKeyLoader

BUNDLE_SCHEMA = "1.1.0"
CONSUMER_MANIFEST_SCHEMA = "1.1.0"
COMPATIBILITY_SCHEMA = "1.1.0"
PREDECESSOR_DESCRIPTOR_SCHEMA = "1.0.0"
RESOURCE_PACKAGE = "tools.reference_corpus_data"
RESOURCE_DIRECTORY = "corpus-files"
PREDECESSOR_DIRECTORY = PurePosixPath("predecessors")
COMPATIBILITY_RESOURCE = PurePosixPath("compatibility.yaml")
CONTRACT_RESOURCES = {
    "reference_bundle_schema_checksum": PurePosixPath("contracts/reference-bundle-1.1.0.schema.json"),
    "consumer_manifest_schema_checksum": PurePosixPath("contracts/consumer-manifest-1.1.0.schema.json"),
    "compatibility_schema_checksum": PurePosixPath("contracts/compatibility-1.1.0.schema.json"),
    "predecessor_descriptor_schema_checksum": PurePosixPath(
        "contracts/predecessor-descriptor-1.0.0.schema.json"
    ),
}
PACKAGE_NAME = "dundercode-engineering-system"
CHECKSUM_PATTERN = re.compile(r"sha256:[0-9a-f]{64}")
RELEASE_TAG_PATTERN = re.compile(
    r"v(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:-(?:alpha|beta|rc)\.[0-9]+)?"
)
SOURCE_COMMIT_PATTERN = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})")
VERSION_PATTERN = re.compile(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:[-+][0-9A-Za-z.-]+)?")
PACKAGE_VERSION_PATTERN = re.compile(
    r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)"
    r"(?:(?:a|b|rc)[0-9]+)?(?:\.post[0-9]+)?(?:\.dev[0-9]+)?"
    r"(?:\+[0-9A-Za-z]+(?:[.-][0-9A-Za-z]+)*)?"
)
CORPUS_PACKAGE_VERSION_PATTERN = re.compile(
    r"(?P<release>(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*))"
    r"(?:(?P<phase>a|b|rc)(?P<number>[0-9]+))?"
)
GIT_SOURCE_PATTERN = re.compile(
    rf"{re.escape(PACKAGE_NAME)} @ git\+https://[^\s@?#]+@(?:[0-9a-fA-F]{{40}}|[0-9a-fA-F]{{64}})"
)
ENTRY_FIELDS = {
    "source",
    "target",
    "collection",
    "classification",
    "indexable",
    "checksum",
}
OPTIONAL_ENTRY_FIELDS = {"document_id", "canonical_id", "metadata_status"}


class CorpusResourceError(ValueError):
    """Raised when packaged corpus resources are malformed or inconsistent."""


class UnsupportedCorpusBundleError(CorpusResourceError):
    """Raised when a consumer manifest belongs to an unsupported corpus snapshot."""


@dataclass(frozen=True, slots=True)
class BundleEntry:
    source: str
    target: PurePosixPath
    collection: str
    classification: str
    indexable: bool
    checksum: str
    content: bytes
    document_id: str | None = None
    canonical_id: str | None = None
    metadata_status: str | None = None


@dataclass(frozen=True, slots=True)
class ReferenceBundle:
    bundle_schema: str
    inventory_schema: str
    corpus_version: str
    release_tag: str
    source_commit: str
    bundle_checksum: str
    entries: tuple[BundleEntry, ...]

    @property
    def source_roots(self) -> tuple[PurePosixPath, ...]:
        roots = {
            PurePosixPath("docs/desys/reference") / entry.collection
            for entry in self.entries
            if entry.target.is_relative_to(PurePosixPath("docs/desys/reference"))
        }
        return tuple(sorted(roots, key=PurePosixPath.as_posix))


@dataclass(frozen=True, slots=True)
class InstalledEntry:
    source: str
    target: PurePosixPath
    collection: str
    classification: str
    distribution: str
    original_checksum: str
    installed_checksum: str
    document_id: str | None = None
    canonical_id: str | None = None


@dataclass(frozen=True, slots=True)
class ConsumerManifest:
    manifest_schema: str
    package_name: str
    package_version: str
    package_source: str
    release_tag: str
    source_commit: str
    corpus_version: str
    bundle_checksum: str
    entries: tuple[InstalledEntry, ...]


@dataclass(frozen=True, slots=True)
class CompatibilityProfile:
    package_version: str
    release_tag: str
    source_commit: str
    corpus_version: str
    inventory_schema: str
    bundle_schema: str
    consumer_manifest_schema: str
    metadata_schema: str
    bundle_checksum: str
    requires_python: str
    platforms: tuple[str, ...]
    direct_predecessor_bundle_checksums: tuple[str, ...]
    predecessor_descriptor_checksums: dict[str, str]
    contract_checksums: dict[str, str]


@dataclass(frozen=True, slots=True)
class DescriptorEntry:
    source: str
    target: PurePosixPath
    collection: str
    classification: str
    indexable: bool
    checksum: str
    document_id: str | None = None
    canonical_id: str | None = None
    metadata_status: str | None = None


@dataclass(frozen=True, slots=True)
class PredecessorDescriptor:
    descriptor_schema: str
    target_bundle_checksum: str
    accepted_manifest_schemas: tuple[str, ...]
    predecessor_package_version: str
    bundle_schema: str
    inventory_schema: str
    corpus_version: str
    release_tag: str
    source_commit: str
    bundle_checksum: str
    entries: tuple[DescriptorEntry, ...]


def load_reference_bundle() -> ReferenceBundle:
    """Load a fully checksum-validated corpus using only importlib resources."""
    package = resources.files(RESOURCE_PACKAGE)
    manifest_bytes = _read_package_resource(package, PurePosixPath("bundle.yaml"))
    data = _load_mapping(manifest_bytes, "packaged corpus bundle")
    _require_fields(
        data,
        {
            "bundle_schema",
            "inventory_schema",
            "corpus_version",
            "release_tag",
            "source_commit",
            "entries",
            "bundle_checksum",
        },
        "packaged corpus bundle",
    )
    if data["bundle_schema"] != BUNDLE_SCHEMA:
        raise CorpusResourceError(f"Unsupported corpus bundle schema: {data['bundle_schema']!r}")
    inventory_schema = _require_version(data["inventory_schema"], "inventory_schema")
    corpus_version = _require_version(data["corpus_version"], "corpus_version")
    release_tag = _require_release_tag(data["release_tag"])
    source_commit = _require_source_commit(data["source_commit"])
    bundle_checksum = _require_checksum(data["bundle_checksum"], "bundle_checksum")
    raw_entries = data["entries"]
    if not isinstance(raw_entries, list) or not raw_entries:
        raise CorpusResourceError("Packaged corpus entries must be a non-empty list.")

    descriptor = {
        "bundle_schema": BUNDLE_SCHEMA,
        "inventory_schema": inventory_schema,
        "corpus_version": corpus_version,
        "release_tag": release_tag,
        "source_commit": source_commit,
        "entries": raw_entries,
    }
    descriptor_bytes = yaml.safe_dump(
        descriptor, sort_keys=False, allow_unicode=False, width=120
    ).encode("utf-8")
    if _checksum(descriptor_bytes) != bundle_checksum:
        raise CorpusResourceError("Packaged corpus bundle checksum does not match its descriptor.")

    entries = tuple(_load_entry(package, item, index) for index, item in enumerate(raw_entries))
    targets = [entry.target for entry in entries]
    sources = [entry.source for entry in entries]
    _require_portable_uniqueness(targets, "Packaged corpus targets")
    _require_portable_uniqueness(sources, "Packaged corpus sources")
    required_legal = {
        PurePosixPath("docs/desys/LICENSE"),
        PurePosixPath("docs/desys/THIRD_PARTY_NOTICES.md"),
    }
    if {entry.target for entry in entries if entry.classification == "legal"} != required_legal:
        raise CorpusResourceError("Packaged corpus must contain exactly the required legal resources.")
    profile = _current_compatibility_profile(package)
    predecessor_resources = {
        _predecessor_resource(checksum) for checksum in profile.direct_predecessor_bundle_checksums
    }
    expected_resources = {
        PurePosixPath("bundle.yaml"),
        COMPATIBILITY_RESOURCE,
        *CONTRACT_RESOURCES.values(),
        *predecessor_resources,
        *(PurePosixPath(RESOURCE_DIRECTORY) / entry.target for entry in entries),
    }
    actual_resources = _collect_package_resources(package)
    if actual_resources != expected_resources:
        raise CorpusResourceError("Packaged corpus resources are missing, stale, or contain unexpected files.")
    bundle = ReferenceBundle(
        BUNDLE_SCHEMA,
        inventory_schema,
        corpus_version,
        release_tag,
        source_commit,
        bundle_checksum,
        entries,
    )
    _validate_bundle_compatibility(package, bundle, profile)
    for checksum in profile.direct_predecessor_bundle_checksums:
        _load_predecessor_descriptor(
            package,
            checksum,
            profile.predecessor_descriptor_checksums[checksum],
            bundle.bundle_checksum,
        )
    return bundle


def load_compatibility_profile(package_version: str | None = None) -> CompatibilityProfile:
    """Load a checksum-validated compatibility profile from package resources."""
    package = resources.files(RESOURCE_PACKAGE)
    if package_version is None:
        profile = _current_compatibility_profile(package)
    else:
        profile = _select_compatibility_profile(package, package_version)
    _validate_contract_checksums(package, profile)
    return profile


def load_predecessor_descriptor(predecessor_bundle_checksum: str) -> PredecessorDescriptor:
    """Load an explicitly declared predecessor authorized for the current target bundle."""
    predecessor_bundle_checksum = _require_checksum(
        predecessor_bundle_checksum, "predecessor_bundle_checksum"
    )
    target = load_reference_bundle()
    package = resources.files(RESOURCE_PACKAGE)
    profile = _current_compatibility_profile(package)
    return _declared_predecessor_descriptor(
        package, profile, predecessor_bundle_checksum, target.bundle_checksum
    )


def _declared_predecessor_descriptor(
    package: Traversable,
    profile: CompatibilityProfile,
    predecessor_bundle_checksum: str,
    target_bundle_checksum: str,
) -> PredecessorDescriptor:
    if predecessor_bundle_checksum not in profile.direct_predecessor_bundle_checksums:
        raise UnsupportedCorpusBundleError(
            "Corpus snapshot is not a declared direct predecessor of the target bundle."
        )
    _validate_contract_checksums(package, profile)
    return _load_predecessor_descriptor(
        package,
        predecessor_bundle_checksum,
        profile.predecessor_descriptor_checksums[predecessor_bundle_checksum],
        target_bundle_checksum,
    )


def validate_predecessor_manifest(
    content: bytes,
    *,
    target_bundle: ReferenceBundle | None = None,
) -> tuple[ConsumerManifest, PredecessorDescriptor]:
    """Validate complete predecessor provenance and ownership before planning."""
    target = target_bundle or load_reference_bundle()
    manifest = _parse_consumer_manifest(content, {CONSUMER_MANIFEST_SCHEMA})
    if manifest.bundle_checksum == target.bundle_checksum:
        raise UnsupportedCorpusBundleError("Consumer manifest belongs to the target bundle, not a predecessor.")
    package = resources.files(RESOURCE_PACKAGE)
    profile = _current_compatibility_profile(package)
    _validate_bundle_compatibility(package, target, profile)
    descriptor = _declared_predecessor_descriptor(
        package, profile, manifest.bundle_checksum, target.bundle_checksum
    )
    if descriptor.target_bundle_checksum != target.bundle_checksum:
        raise UnsupportedCorpusBundleError("Predecessor descriptor does not authorize this target bundle.")
    _validate_predecessor_manifest(manifest, descriptor)
    return manifest, descriptor


def load_consumer_manifest(
    content: bytes,
    *,
    expected_bundle_checksum: str | None = None,
) -> ConsumerManifest:
    """Strictly validate a consumer manifest before it can assert ownership."""
    manifest = _parse_consumer_manifest(content, {CONSUMER_MANIFEST_SCHEMA})
    if expected_bundle_checksum is not None and manifest.bundle_checksum != expected_bundle_checksum:
        raise UnsupportedCorpusBundleError("Consumer manifest uses an unsupported prior corpus bundle.")
    profile = load_compatibility_profile(manifest.package_version)
    _validate_manifest_compatibility(manifest, profile)
    return manifest


def _parse_consumer_manifest(content: bytes, accepted_schemas: set[str]) -> ConsumerManifest:
    data = _load_mapping(content, "consumer corpus manifest")
    required = {
        "manifest_schema",
        "package_name",
        "package_version",
        "package_source",
        "release_tag",
        "source_commit",
        "corpus_version",
        "bundle_checksum",
        "entries",
    }
    _require_fields(data, required, "consumer corpus manifest")
    manifest_schema = _require_version(data["manifest_schema"], "manifest_schema")
    if manifest_schema not in accepted_schemas:
        raise CorpusResourceError(f"Unsupported consumer manifest schema: {data['manifest_schema']!r}")
    package_name = _require_text(data["package_name"], "package_name")
    if package_name != PACKAGE_NAME:
        raise CorpusResourceError(f"package_name must be {PACKAGE_NAME!r}.")
    package_version = _require_package_version(data["package_version"])
    package_source = _require_package_source(data["package_source"], package_version)
    release_tag = _require_release_tag(data["release_tag"])
    if release_tag != _release_tag_for_package_version(package_version):
        raise CorpusResourceError("release_tag does not match package_version.")
    source_commit = _require_source_commit(data["source_commit"])
    corpus_version = _require_version(data["corpus_version"], "corpus_version")
    bundle_checksum = _require_checksum(data["bundle_checksum"], "bundle_checksum")
    raw_entries = data["entries"]
    if not isinstance(raw_entries, list) or not raw_entries:
        raise CorpusResourceError("Consumer manifest entries must be a non-empty list.")
    entries = tuple(_load_installed_entry(value, index) for index, value in enumerate(raw_entries))
    targets = [entry.target for entry in entries]
    sources = [entry.source for entry in entries]
    _require_portable_uniqueness(targets, "Consumer manifest targets")
    _require_portable_uniqueness(sources, "Consumer manifest sources")
    manifest = ConsumerManifest(
        manifest_schema,
        package_name,
        package_version,
        package_source,
        release_tag,
        source_commit,
        corpus_version,
        bundle_checksum,
        entries,
    )
    return manifest


def render_consumer_manifest(
    bundle: ReferenceBundle,
    *,
    package_name: str,
    package_version: str,
    package_source: str,
) -> bytes:
    """Render canonical ownership and provenance for installed corpus files."""
    if package_name != PACKAGE_NAME:
        raise CorpusResourceError(f"package_name must be {PACKAGE_NAME!r}.")
    if bundle.release_tag != _release_tag_for_package_version(package_version):
        raise CorpusResourceError("Packaged release_tag does not match package_version.")
    profile = load_compatibility_profile(package_version)
    _validate_bundle_compatibility(resources.files(RESOURCE_PACKAGE), bundle, profile)
    payload: dict[str, Any] = {
        "manifest_schema": CONSUMER_MANIFEST_SCHEMA,
        "package_name": package_name,
        "package_version": package_version,
        "package_source": package_source,
        "release_tag": bundle.release_tag,
        "source_commit": bundle.source_commit,
        "corpus_version": bundle.corpus_version,
        "bundle_checksum": bundle.bundle_checksum,
        "entries": [],
    }
    for entry in bundle.entries:
        item = {
            "source": entry.source,
            "target": entry.target.as_posix(),
            "collection": entry.collection,
            "classification": entry.classification,
            "distribution": "approved",
            "original_checksum": entry.checksum,
            "installed_checksum": entry.checksum,
        }
        if entry.document_id is not None:
            item["document_id"] = entry.document_id
        if entry.canonical_id is not None:
            item["canonical_id"] = entry.canonical_id
        payload["entries"].append(item)
    return yaml.safe_dump(payload, sort_keys=False, allow_unicode=False, width=120).encode("utf-8")


def validate_target(value: Any, field: str = "target") -> PurePosixPath:
    """Return an allowlisted, normalized consumer corpus target."""
    path = _require_safe_path(value, field)
    try:
        validate_portable_target(path)
    except InventoryError as error:
        raise CorpusResourceError(f"{field} is not portable: {error}") from error
    legal_targets = {
        PurePosixPath("docs/desys/LICENSE"),
        PurePosixPath("docs/desys/THIRD_PARTY_NOTICES.md"),
    }
    reference_root = PurePosixPath("docs/desys/reference")
    if path not in legal_targets and (not path.is_relative_to(reference_root) or path == reference_root):
        raise CorpusResourceError(f"{field} is outside the managed corpus area: {value!r}")
    return path


def _load_entry(package: Traversable, value: Any, index: int) -> BundleEntry:
    context = f"packaged corpus entry {index}"
    if not isinstance(value, dict):
        raise CorpusResourceError(f"{context} must be a mapping.")
    _require_fields(value, ENTRY_FIELDS, context, optional=OPTIONAL_ENTRY_FIELDS)
    source_path = _require_safe_path(value["source"], f"{context}.source")
    target = validate_target(value["target"], f"{context}.target")
    collection = _require_text(value["collection"], f"{context}.collection")
    classification = _require_text(value["classification"], f"{context}.classification")
    if type(value["indexable"]) is not bool:
        raise CorpusResourceError(f"{context}.indexable must be a boolean.")
    checksum = _require_checksum(value["checksum"], f"{context}.checksum")
    _validate_target_metadata(target, collection, classification, value["indexable"], context)
    optional = {
        field: _require_text(value[field], f"{context}.{field}") if field in value else None
        for field in OPTIONAL_ENTRY_FIELDS
    }
    content = _read_package_resource(package, PurePosixPath(RESOURCE_DIRECTORY) / target)
    if _checksum(content) != checksum:
        raise CorpusResourceError(f"Packaged corpus resource checksum mismatch: {target}")
    return BundleEntry(
        source=source_path.as_posix(),
        target=target,
        collection=collection,
        classification=classification,
        indexable=value["indexable"],
        checksum=checksum,
        content=content,
        document_id=optional["document_id"],
        canonical_id=optional["canonical_id"],
        metadata_status=optional["metadata_status"],
    )


def _load_installed_entry(value: Any, index: int) -> InstalledEntry:
    context = f"consumer manifest entry {index}"
    if not isinstance(value, dict):
        raise CorpusResourceError(f"{context} must be a mapping.")
    required = {
        "source",
        "target",
        "collection",
        "classification",
        "distribution",
        "original_checksum",
        "installed_checksum",
    }
    optional = {"document_id", "canonical_id"}
    _require_fields(value, required, context, optional=optional)
    distribution = _require_text(value["distribution"], f"{context}.distribution")
    if distribution != "approved":
        raise CorpusResourceError(f"{context}.distribution must be 'approved'.")
    target = validate_target(value["target"], f"{context}.target")
    collection = _require_text(value["collection"], f"{context}.collection")
    classification = _require_text(value["classification"], f"{context}.classification")
    _validate_target_metadata(target, collection, classification, False, context, check_indexable=False)
    return InstalledEntry(
        source=_require_safe_path(value["source"], f"{context}.source").as_posix(),
        target=target,
        collection=collection,
        classification=classification,
        distribution=distribution,
        original_checksum=_require_checksum(value["original_checksum"], f"{context}.original_checksum"),
        installed_checksum=_require_checksum(value["installed_checksum"], f"{context}.installed_checksum"),
        document_id=(
            _require_text(value["document_id"], f"{context}.document_id") if "document_id" in value else None
        ),
        canonical_id=(
            _require_text(value["canonical_id"], f"{context}.canonical_id") if "canonical_id" in value else None
        ),
    )


def _predecessor_resource(bundle_checksum: str) -> PurePosixPath:
    checksum = _require_checksum(bundle_checksum, "predecessor bundle checksum")
    return PREDECESSOR_DIRECTORY / f"sha256-{checksum.removeprefix('sha256:')}.yaml"


def _load_predecessor_descriptor(
    package: Traversable,
    predecessor_bundle_checksum: str,
    expected_descriptor_checksum: str,
    target_bundle_checksum: str,
) -> PredecessorDescriptor:
    resource = _predecessor_resource(predecessor_bundle_checksum)
    content = _read_package_resource(package, resource)
    if _checksum(content) != expected_descriptor_checksum:
        raise CorpusResourceError(f"Packaged predecessor descriptor checksum mismatch: {resource}")
    data = _load_mapping(content, "predecessor descriptor")
    required = {
        "predecessor_descriptor_schema",
        "target_bundle_checksum",
        "accepted_manifest_schemas",
        "predecessor_package_version",
        "bundle_schema",
        "inventory_schema",
        "corpus_version",
        "release_tag",
        "source_commit",
        "entries",
        "bundle_checksum",
    }
    _require_fields(data, required, "predecessor descriptor")
    if data["predecessor_descriptor_schema"] != PREDECESSOR_DESCRIPTOR_SCHEMA:
        raise CorpusResourceError(
            f"Unsupported predecessor descriptor schema: {data['predecessor_descriptor_schema']!r}"
        )
    authorized_target = _require_checksum(data["target_bundle_checksum"], "target_bundle_checksum")
    if authorized_target != target_bundle_checksum:
        raise CorpusResourceError("Predecessor descriptor does not authorize the current target bundle.")
    if authorized_target == predecessor_bundle_checksum:
        raise CorpusResourceError("Predecessor descriptor cannot authorize its own bundle.")
    accepted = data["accepted_manifest_schemas"]
    if not isinstance(accepted, list) or not accepted or len(accepted) != len(set(accepted)):
        raise CorpusResourceError("accepted_manifest_schemas must be a non-empty unique list.")
    accepted_schemas = tuple(
        _require_version(value, "accepted_manifest_schemas") for value in accepted
    )
    if any(schema != CONSUMER_MANIFEST_SCHEMA for schema in accepted_schemas):
        raise CorpusResourceError("Predecessor descriptor accepts an unsupported manifest schema.")
    predecessor_package_version = _require_package_version(data["predecessor_package_version"])
    bundle_schema = _require_version(data["bundle_schema"], "bundle_schema")
    if bundle_schema != BUNDLE_SCHEMA:
        raise CorpusResourceError(f"Unsupported predecessor bundle schema: {bundle_schema!r}")
    inventory_schema = _require_version(data["inventory_schema"], "inventory_schema")
    corpus_version = _require_version(data["corpus_version"], "corpus_version")
    release_tag = _require_release_tag(data["release_tag"])
    if release_tag != _release_tag_for_package_version(predecessor_package_version):
        raise CorpusResourceError("Predecessor release_tag does not match its package version.")
    source_commit = _require_source_commit(data["source_commit"])
    bundle_checksum = _require_checksum(data["bundle_checksum"], "bundle_checksum")
    if bundle_checksum != predecessor_bundle_checksum:
        raise CorpusResourceError("Predecessor descriptor checksum does not match its resource name.")
    raw_entries = data["entries"]
    if not isinstance(raw_entries, list) or not raw_entries:
        raise CorpusResourceError("Predecessor descriptor entries must be a non-empty list.")
    bundle_payload = {
        "bundle_schema": bundle_schema,
        "inventory_schema": inventory_schema,
        "corpus_version": corpus_version,
        "release_tag": release_tag,
        "source_commit": source_commit,
        "entries": raw_entries,
    }
    bundle_bytes = yaml.safe_dump(
        bundle_payload, sort_keys=False, allow_unicode=False, width=120
    ).encode("utf-8")
    if _checksum(bundle_bytes) != bundle_checksum:
        raise CorpusResourceError("Predecessor bundle checksum does not match its descriptor.")
    entries = tuple(_load_descriptor_entry(value, index) for index, value in enumerate(raw_entries))
    _require_portable_uniqueness([entry.target for entry in entries], "Predecessor descriptor targets")
    _require_portable_uniqueness([entry.source for entry in entries], "Predecessor descriptor sources")
    return PredecessorDescriptor(
        descriptor_schema=PREDECESSOR_DESCRIPTOR_SCHEMA,
        target_bundle_checksum=authorized_target,
        accepted_manifest_schemas=accepted_schemas,
        predecessor_package_version=predecessor_package_version,
        bundle_schema=bundle_schema,
        inventory_schema=inventory_schema,
        corpus_version=corpus_version,
        release_tag=release_tag,
        source_commit=source_commit,
        bundle_checksum=bundle_checksum,
        entries=entries,
    )


def _load_descriptor_entry(value: Any, index: int) -> DescriptorEntry:
    context = f"predecessor descriptor entry {index}"
    if not isinstance(value, dict):
        raise CorpusResourceError(f"{context.capitalize()} must be a mapping.")
    _require_fields(value, ENTRY_FIELDS, context, optional=OPTIONAL_ENTRY_FIELDS)
    source = _require_safe_path(value["source"], f"{context}.source").as_posix()
    target = validate_target(value["target"], f"{context}.target")
    collection = _require_text(value["collection"], f"{context}.collection")
    classification = _require_text(value["classification"], f"{context}.classification")
    if type(value["indexable"]) is not bool:
        raise CorpusResourceError(f"{context}.indexable must be a boolean.")
    _validate_target_metadata(target, collection, classification, value["indexable"], context)
    return DescriptorEntry(
        source=source,
        target=target,
        collection=collection,
        classification=classification,
        indexable=value["indexable"],
        checksum=_require_checksum(value["checksum"], f"{context}.checksum"),
        document_id=(
            _require_text(value["document_id"], f"{context}.document_id")
            if "document_id" in value
            else None
        ),
        canonical_id=(
            _require_text(value["canonical_id"], f"{context}.canonical_id")
            if "canonical_id" in value
            else None
        ),
        metadata_status=(
            _require_text(value["metadata_status"], f"{context}.metadata_status")
            if "metadata_status" in value
            else None
        ),
    )


def _validate_predecessor_manifest(
    manifest: ConsumerManifest,
    descriptor: PredecessorDescriptor,
) -> None:
    provenance = (
        manifest.manifest_schema,
        manifest.package_version,
        manifest.release_tag,
        manifest.source_commit,
        manifest.corpus_version,
        manifest.bundle_checksum,
    )
    expected_provenance = (
        manifest.manifest_schema if manifest.manifest_schema in descriptor.accepted_manifest_schemas else None,
        descriptor.predecessor_package_version,
        descriptor.release_tag,
        descriptor.source_commit,
        descriptor.corpus_version,
        descriptor.bundle_checksum,
    )
    if provenance != expected_provenance:
        raise CorpusResourceError("Consumer manifest provenance does not match its predecessor descriptor.")
    expected_entries = tuple(
        InstalledEntry(
            source=entry.source,
            target=entry.target,
            collection=entry.collection,
            classification=entry.classification,
            distribution="approved",
            original_checksum=entry.checksum,
            installed_checksum=entry.checksum,
            document_id=entry.document_id,
            canonical_id=entry.canonical_id,
        )
        for entry in descriptor.entries
    )
    if manifest.entries != expected_entries:
        raise CorpusResourceError("Consumer manifest entries do not match its predecessor descriptor.")


def _load_mapping(content: bytes, context: str) -> dict[str, Any]:
    try:
        text = content.decode("utf-8")
        data = yaml.load(text, Loader=UniqueKeyLoader)
    except (UnicodeError, yaml.YAMLError) as error:
        raise CorpusResourceError(f"Invalid {context} YAML: {error}") from error
    if not isinstance(data, dict) or any(not isinstance(key, str) for key in data):
        raise CorpusResourceError(f"{context.capitalize()} must be a string-keyed mapping.")
    return data


def _current_compatibility_profile(package: Traversable) -> CompatibilityProfile:
    installed_version, requires_python = _installed_package_contract()
    profile = _select_compatibility_profile(package, installed_version)
    if profile.requires_python != requires_python:
        raise CorpusResourceError("Compatibility profile requires_python does not match package metadata.")
    return profile


def _installed_package_contract() -> tuple[str, str]:
    try:
        installed_version = version(PACKAGE_NAME)
        requires_python = metadata(PACKAGE_NAME).get("Requires-Python")
    except PackageNotFoundError as error:
        raise CorpusResourceError("DESys package metadata is unavailable.") from error
    if requires_python is None:
        raise CorpusResourceError("DESys package metadata has no Requires-Python contract.")
    return installed_version, requires_python


def _select_compatibility_profile(package: Traversable, package_version: str) -> CompatibilityProfile:
    matrix = _load_mapping(
        _read_package_resource(package, COMPATIBILITY_RESOURCE),
        "distribution compatibility matrix",
    )
    _require_fields(
        matrix,
        {"compatibility_schema", "package_name", "profiles"},
        "distribution compatibility matrix",
    )
    if matrix["compatibility_schema"] != COMPATIBILITY_SCHEMA:
        raise CorpusResourceError(f"Unsupported compatibility schema: {matrix['compatibility_schema']!r}")
    if matrix["package_name"] != PACKAGE_NAME:
        raise CorpusResourceError(f"Compatibility package_name must be {PACKAGE_NAME!r}.")
    raw_profiles = matrix["profiles"]
    if not isinstance(raw_profiles, list) or not raw_profiles:
        raise CorpusResourceError("Compatibility profiles must be a non-empty list.")
    profiles = tuple(_load_compatibility_profile(item, index) for index, item in enumerate(raw_profiles))
    versions = [profile.package_version for profile in profiles]
    if len(versions) != len(set(versions)):
        raise CorpusResourceError("Compatibility profile package versions must be unique.")
    selected = [profile for profile in profiles if profile.package_version == package_version]
    if not selected:
        raise UnsupportedCorpusBundleError(
            f"No compatibility profile exists for package version {package_version!r}."
        )
    return selected[0]


def _load_compatibility_profile(value: Any, index: int) -> CompatibilityProfile:
    context = f"compatibility profile {index}"
    if not isinstance(value, dict):
        raise CorpusResourceError(f"{context.capitalize()} must be a mapping.")
    required = {
        "package_version",
        "release_tag",
        "source_commit",
        "corpus_version",
        "inventory_schema",
        "bundle_schema",
        "consumer_manifest_schema",
        "metadata_schema",
        "bundle_checksum",
        "requires_python",
        "platforms",
        "direct_predecessors",
        *CONTRACT_RESOURCES,
    }
    _require_fields(value, required, context)
    platforms = value["platforms"]
    if (
        not isinstance(platforms, list)
        or not platforms
        or any(platform not in {"linux", "macos", "windows"} for platform in platforms)
        or len(platforms) != len(set(platforms))
    ):
        raise CorpusResourceError(f"{context}.platforms must contain unique supported platform names.")
    predecessors = value["direct_predecessors"]
    if not isinstance(predecessors, list):
        raise CorpusResourceError(f"{context}.direct_predecessors must be a list.")
    predecessor_pairs: list[tuple[str, str]] = []
    for predecessor_index, predecessor in enumerate(predecessors):
        predecessor_context = f"{context}.direct_predecessors[{predecessor_index}]"
        if not isinstance(predecessor, dict):
            raise CorpusResourceError(f"{predecessor_context} must be a mapping.")
        _require_fields(predecessor, {"bundle_checksum", "descriptor_checksum"}, predecessor_context)
        predecessor_pairs.append(
            (
                _require_checksum(predecessor["bundle_checksum"], f"{predecessor_context}.bundle_checksum"),
                _require_checksum(
                    predecessor["descriptor_checksum"], f"{predecessor_context}.descriptor_checksum"
                ),
            )
        )
    predecessor_checksums = tuple(bundle_checksum for bundle_checksum, _ in predecessor_pairs)
    descriptor_checksums = tuple(descriptor_checksum for _, descriptor_checksum in predecessor_pairs)
    if len(predecessor_checksums) != len(set(predecessor_checksums)):
        raise CorpusResourceError(f"{context}.direct_predecessors bundle checksums must be unique.")
    if len(descriptor_checksums) != len(set(descriptor_checksums)):
        raise CorpusResourceError(f"{context}.direct_predecessors descriptor checksums must be unique.")
    contract_checksums = {
        field: _require_checksum(value[field], f"{context}.{field}") for field in CONTRACT_RESOURCES
    }
    profile = CompatibilityProfile(
        package_version=_require_package_version(value["package_version"]),
        release_tag=_require_release_tag(value["release_tag"]),
        source_commit=_require_source_commit(value["source_commit"]),
        corpus_version=_require_version(value["corpus_version"], f"{context}.corpus_version"),
        inventory_schema=_require_version(value["inventory_schema"], f"{context}.inventory_schema"),
        bundle_schema=_require_version(value["bundle_schema"], f"{context}.bundle_schema"),
        consumer_manifest_schema=_require_version(
            value["consumer_manifest_schema"], f"{context}.consumer_manifest_schema"
        ),
        metadata_schema=_require_version(value["metadata_schema"], f"{context}.metadata_schema"),
        bundle_checksum=_require_checksum(value["bundle_checksum"], f"{context}.bundle_checksum"),
        requires_python=_require_text(value["requires_python"], f"{context}.requires_python"),
        platforms=tuple(platforms),
        direct_predecessor_bundle_checksums=predecessor_checksums,
        predecessor_descriptor_checksums=dict(predecessor_pairs),
        contract_checksums=contract_checksums,
    )
    if profile.release_tag != _release_tag_for_package_version(profile.package_version):
        raise CorpusResourceError(f"{context}.release_tag does not match its package_version.")
    if profile.bundle_checksum in profile.direct_predecessor_bundle_checksums:
        raise CorpusResourceError(f"{context} cannot list its own bundle as a direct predecessor.")
    return profile


def _validate_bundle_compatibility(
    package: Traversable,
    bundle: ReferenceBundle,
    profile: CompatibilityProfile,
) -> None:
    actual = (
        bundle.release_tag,
        bundle.source_commit,
        bundle.corpus_version,
        bundle.inventory_schema,
        bundle.bundle_schema,
        bundle.bundle_checksum,
    )
    expected = (
        profile.release_tag,
        profile.source_commit,
        profile.corpus_version,
        profile.inventory_schema,
        profile.bundle_schema,
        profile.bundle_checksum,
    )
    if actual != expected:
        raise CorpusResourceError("Reference bundle does not match its compatibility profile.")
    if profile.consumer_manifest_schema != CONSUMER_MANIFEST_SCHEMA:
        raise CorpusResourceError("Compatibility profile does not match the supported consumer manifest schema.")
    _validate_contract_checksums(package, profile)
    metadata_entries = [
        entry
        for entry in bundle.entries
        if entry.target.as_posix()
        == "docs/desys/reference/knowledge/architecture/metadata/desys-metadata.schema.json"
    ]
    if len(metadata_entries) != 1:
        raise CorpusResourceError("Reference bundle must contain exactly one metadata schema resource.")
    try:
        metadata_schema = json.loads(metadata_entries[0].content)
        metadata_version = metadata_schema["properties"]["metadata_schema"]["const"]
    except (KeyError, TypeError, ValueError) as error:
        raise CorpusResourceError("Packaged metadata schema has no valid version contract.") from error
    if metadata_version != profile.metadata_schema:
        raise CorpusResourceError("Packaged metadata schema does not match its compatibility profile.")


def _validate_contract_checksums(
    package: Traversable,
    profile: CompatibilityProfile,
) -> None:
    for field, path in CONTRACT_RESOURCES.items():
        if _checksum(_read_package_resource(package, path)) != profile.contract_checksums[field]:
            raise CorpusResourceError(f"Packaged contract checksum mismatch: {path}")


def _validate_manifest_compatibility(
    manifest: ConsumerManifest,
    profile: CompatibilityProfile,
) -> None:
    if (
        manifest.bundle_checksum != profile.bundle_checksum
        or manifest.manifest_schema != profile.consumer_manifest_schema
    ):
        raise UnsupportedCorpusBundleError("Consumer manifest is not supported by the compatibility matrix.")


def _require_fields(
    value: dict[Any, Any],
    required: set[str],
    context: str,
    *,
    optional: set[str] = frozenset(),
) -> None:
    if any(not isinstance(key, str) for key in value):
        raise CorpusResourceError(f"{context.capitalize()} must use string field names.")
    missing = sorted(required - set(value))
    unknown = sorted(set(value) - required - optional)
    if missing:
        raise CorpusResourceError(f"{context.capitalize()} is missing field(s): {', '.join(missing)}")
    if unknown:
        raise CorpusResourceError(f"{context.capitalize()} has unknown field(s): {', '.join(unknown)}")


def _require_safe_path(value: Any, field: str) -> PurePosixPath:
    text = _require_text(value, field)
    path = PurePosixPath(text)
    if (
        path.is_absolute()
        or text != path.as_posix()
        or not path.parts
        or any(part in {"", ".", ".."} for part in path.parts)
        or "\\" in text
        or "\0" in text
    ):
        raise CorpusResourceError(f"{field} must be a normalized safe relative path.")
    return path


def _require_portable_uniqueness(values: list[str | PurePosixPath], context: str) -> None:
    keys = [_portable_path_key(value) for value in values]
    if len(keys) != len(set(keys)):
        raise CorpusResourceError(f"{context} must be unique across supported filesystems.")


def _portable_path_key(value: str | PurePosixPath) -> str:
    path = value if isinstance(value, PurePosixPath) else PurePosixPath(value)
    return "/".join(part.casefold() for part in path.parts)


def _read_package_resource(package: Traversable, relative: PurePosixPath) -> bytes:
    resource = package.joinpath(*relative.parts)
    if isinstance(package, Path) and isinstance(resource, Path):
        return _read_filesystem_resource(package, resource, relative)
    try:
        if not resource.is_file():
            raise CorpusResourceError(f"Packaged corpus resource is not a regular file: {relative}")
        return resource.read_bytes()
    except (FileNotFoundError, IsADirectoryError, OSError) as error:
        raise CorpusResourceError(f"Packaged corpus resource is unavailable: {relative}") from error


def _read_filesystem_resource(package: Path, resource: Path, relative: PurePosixPath) -> bytes:
    current = package
    try:
        package_status = current.lstat()
        if stat.S_ISLNK(package_status.st_mode) or not stat.S_ISDIR(package_status.st_mode):
            raise CorpusResourceError("Packaged corpus root is not a regular directory.")
        for index, part in enumerate(relative.parts):
            current /= part
            status = current.lstat()
            if stat.S_ISLNK(status.st_mode):
                raise CorpusResourceError(f"Packaged corpus resource contains a symlink: {relative}")
            if index < len(relative.parts) - 1:
                if not stat.S_ISDIR(status.st_mode):
                    raise CorpusResourceError(f"Packaged corpus resource ancestor is not a directory: {relative}")
            elif not stat.S_ISREG(status.st_mode):
                raise CorpusResourceError(f"Packaged corpus resource is not a regular file: {relative}")
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(resource, flags)
    except (FileNotFoundError, NotADirectoryError, OSError) as error:
        raise CorpusResourceError(f"Packaged corpus resource is unavailable: {relative}") from error
    try:
        status = os.fstat(descriptor)
        if not stat.S_ISREG(status.st_mode):
            raise CorpusResourceError(f"Packaged corpus resource is not a regular file: {relative}")
        if status.st_mode & 0o111:
            raise CorpusResourceError(f"Packaged corpus resource is executable: {relative}")
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = -1
            return stream.read()
    except OSError as error:
        raise CorpusResourceError(f"Unable to read packaged corpus resource: {relative}") from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def _collect_package_resources(package: Traversable) -> set[PurePosixPath]:
    found: set[PurePosixPath] = set()

    def visit(directory: Traversable, parent: PurePosixPath) -> None:
        try:
            children = tuple(directory.iterdir())
        except OSError as error:
            raise CorpusResourceError(f"Unable to enumerate packaged corpus resources: {parent}") from error
        for child in children:
            relative = parent / child.name
            if isinstance(child, Path) and child.is_symlink():
                raise CorpusResourceError(f"Packaged corpus resource contains a symlink: {relative}")
            if child.name == "__pycache__":
                continue
            if child.is_dir():
                visit(child, relative)
            elif child.is_file():
                if relative != PurePosixPath("__init__.py"):
                    found.add(relative)
            else:
                raise CorpusResourceError(f"Packaged corpus resource is not a regular file: {relative}")

    visit(package, PurePosixPath())
    return found


def _require_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip() or any(char in value for char in "\r\n\0"):
        raise CorpusResourceError(f"{field} must be a non-empty single-line string.")
    return value


def _require_version(value: Any, field: str) -> str:
    text = _require_text(value, field)
    if VERSION_PATTERN.fullmatch(text) is None:
        raise CorpusResourceError(f"{field} must be a semantic version.")
    return text


def _require_checksum(value: Any, field: str) -> str:
    text = _require_text(value, field)
    if CHECKSUM_PATTERN.fullmatch(text) is None:
        raise CorpusResourceError(f"{field} must be a lowercase SHA-256 checksum.")
    return text


def _require_release_tag(value: Any) -> str:
    text = _require_text(value, "release_tag")
    if RELEASE_TAG_PATTERN.fullmatch(text) is None:
        raise CorpusResourceError("release_tag must be an immutable DESys release tag.")
    return text


def _require_source_commit(value: Any) -> str:
    text = _require_text(value, "source_commit")
    if SOURCE_COMMIT_PATTERN.fullmatch(text) is None:
        raise CorpusResourceError("source_commit must be a full lowercase Git commit SHA.")
    return text


def _release_tag_for_package_version(package_version: str) -> str:
    match = CORPUS_PACKAGE_VERSION_PATTERN.fullmatch(package_version)
    if match is None:
        raise CorpusResourceError("package_version cannot be represented by a corpus release tag.")
    phase = match.group("phase")
    if phase is None:
        return f"v{match.group('release')}"
    phase_name = {"a": "alpha", "b": "beta", "rc": "rc"}[phase]
    return f"v{match.group('release')}-{phase_name}.{match.group('number')}"


def _require_package_version(value: Any) -> str:
    text = _require_text(value, "package_version")
    if text != "unreleased" and PACKAGE_VERSION_PATTERN.fullmatch(text) is None:
        raise CorpusResourceError("package_version must be a valid DESys package version.")
    return text


def _require_package_source(value: Any, package_version: str) -> str:
    text = _require_text(value, "package_source")
    if text == f"{PACKAGE_NAME}=={package_version}" or GIT_SOURCE_PATTERN.fullmatch(text):
        return text
    path = PurePosixPath(text)
    if (
        path.suffix != ".whl"
        or path.is_absolute()
        or text != path.as_posix()
        or ".." in path.parts
        or ".." in text
        or "\\" in text
        or any(not part for part in path.parts)
    ):
        raise CorpusResourceError("package_source is not an immutable supported DESys source.")
    return text


def _validate_target_metadata(
    target: PurePosixPath,
    collection: str,
    classification: str,
    indexable: bool,
    context: str,
    *,
    check_indexable: bool = True,
) -> None:
    reference_root = PurePosixPath("docs/desys/reference")
    if target.is_relative_to(reference_root):
        if len(target.parts) < 5 or target.parts[3] != collection:
            raise CorpusResourceError(f"{context}.collection does not match its reference target.")
        return
    if collection != "legal" or classification != "legal" or (check_indexable and indexable):
        raise CorpusResourceError(f"{context} has inconsistent legal resource metadata.")


def _checksum(content: bytes) -> str:
    return f"sha256:{hashlib.sha256(content).hexdigest()}"
