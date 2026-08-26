"""Load and validate the immutable reference corpus package resources."""

from __future__ import annotations

import hashlib
import os
import re
import stat
from dataclasses import dataclass
from importlib import resources
from importlib.resources.abc import Traversable
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

from tools.build_corpus_inventory import InventoryError, validate_portable_target
from tools.desys_metadata import UniqueKeyLoader

BUNDLE_SCHEMA = "1.1.0"
CONSUMER_MANIFEST_SCHEMA = "1.1.0"
RESOURCE_PACKAGE = "tools.reference_corpus_data"
RESOURCE_DIRECTORY = "corpus-files"
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
    package_name: str
    package_version: str
    package_source: str
    release_tag: str
    source_commit: str
    corpus_version: str
    bundle_checksum: str
    entries: tuple[InstalledEntry, ...]


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
    expected_resources = {
        PurePosixPath("bundle.yaml"),
        *(PurePosixPath(RESOURCE_DIRECTORY) / entry.target for entry in entries),
    }
    actual_resources = _collect_package_resources(package)
    if actual_resources != expected_resources:
        raise CorpusResourceError("Packaged corpus resources are missing, stale, or contain unexpected files.")
    return ReferenceBundle(
        BUNDLE_SCHEMA,
        inventory_schema,
        corpus_version,
        release_tag,
        source_commit,
        bundle_checksum,
        entries,
    )


def load_consumer_manifest(
    content: bytes,
    *,
    expected_bundle_checksum: str | None = None,
) -> ConsumerManifest:
    """Strictly validate a consumer manifest before it can assert ownership."""
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
    if data["manifest_schema"] != CONSUMER_MANIFEST_SCHEMA:
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
    if expected_bundle_checksum is not None and bundle_checksum != expected_bundle_checksum:
        raise UnsupportedCorpusBundleError("Consumer manifest uses an unsupported prior corpus bundle.")
    raw_entries = data["entries"]
    if not isinstance(raw_entries, list) or not raw_entries:
        raise CorpusResourceError("Consumer manifest entries must be a non-empty list.")
    entries = tuple(_load_installed_entry(value, index) for index, value in enumerate(raw_entries))
    targets = [entry.target for entry in entries]
    sources = [entry.source for entry in entries]
    _require_portable_uniqueness(targets, "Consumer manifest targets")
    _require_portable_uniqueness(sources, "Consumer manifest sources")
    return ConsumerManifest(
        package_name,
        package_version,
        package_source,
        release_tag,
        source_commit,
        corpus_version,
        bundle_checksum,
        entries,
    )


def render_consumer_manifest(
    bundle: ReferenceBundle,
    *,
    package_name: str,
    package_version: str,
    package_source: str,
) -> bytes:
    """Render canonical ownership and provenance for installed corpus files."""
    if bundle.release_tag != _release_tag_for_package_version(package_version):
        raise CorpusResourceError("Packaged release_tag does not match package_version.")
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


def _load_mapping(content: bytes, context: str) -> dict[str, Any]:
    try:
        text = content.decode("utf-8")
        data = yaml.load(text, Loader=UniqueKeyLoader)
    except (UnicodeError, yaml.YAMLError) as error:
        raise CorpusResourceError(f"Invalid {context} YAML: {error}") from error
    if not isinstance(data, dict) or any(not isinstance(key, str) for key in data):
        raise CorpusResourceError(f"{context.capitalize()} must be a string-keyed mapping.")
    return data


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
