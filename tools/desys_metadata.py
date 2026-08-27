"""Parsing and repository-level validation for canonical DESys metadata."""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from yaml.constructor import ConstructorError

SCHEMA_VERSION = "1.0.0"

DOCUMENT_ID_PATTERN = re.compile(
    r"^(ADR|DAR|DCSG|DEA|DEC|DEKG|DEM|DES|DET|DEP|DSB|DSK|DSP|GUIDE|PRD|RFC)-[0-9]{4}$"
)
CANONICAL_ID_PATTERN = re.compile(
    r"^(adr|dar|dcsg|dea|dec|dekg|dem|des|det|dep|dsb|dsk|dsp|guide|prd|rfc)"
    r"(?:\.[a-z0-9]+(?:-[a-z0-9]+)*){2,}$"
)
LEGACY_CANONICAL_ID_PATTERN = re.compile(
    r"^(adr|dar|dcsg|dea|dec|dekg|dem|des|det|dep|dsb|dsk|dsp|guide|prd|rfc)"
    r"(?:\.[a-z0-9]+(?:-[a-z0-9]+)*){1,}$"
)
VERSION_PATTERN = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")
MANAGED_FILENAME_PATTERN = re.compile(
    r"^(?P<document_id>(?:ADR|DAR|DCSG|DEA|DEC|DEKG|DEM|DES|DET|DEP|DSB|DSK|DSP|GUIDE|PRD|RFC)-[0-9]{4})(?:-.+)?\.md$"
)

REQUIRED_FIELDS = (
    "metadata_schema",
    "document_id",
    "canonical_id",
    "title",
    "node_type",
    "document_class",
    "version",
    "status",
    "language",
    "owner",
)
OPTIONAL_FIELDS = (
    "domain",
    "discipline",
    "architecture_model",
    "authors",
    "reviewers",
    "applies_to",
    "tags",
    "aliases",
    "legacy_status",
    "relationships",
)
NODE_TYPES = {
    "architecture",
    "assessment",
    "canon",
    "decision",
    "guide",
    "method",
    "process",
    "product-requirement",
    "proposal",
    "skill",
    "specification",
    "standard",
    "style-guide",
    "template",
}
DOCUMENT_CLASSES = {"informative", "normative", "operational", "reference"}
STATUSES = {"approved", "canonical", "deprecated", "draft", "published", "review"}
RELATIONSHIP_TYPES = {
    "belongs_to",
    "child",
    "consumes",
    "depends_on",
    "derives_from",
    "defines",
    "explains",
    "extends",
    "implements",
    "owns",
    "parent",
    "produces",
    "realizes",
    "references",
    "related",
    "specializes",
    "supersedes",
    "triggers",
    "validates",
}


class FrontMatterError(ValueError):
    """Raised when a document has missing or malformed YAML front matter."""


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _construct_unique_mapping(
    loader: UniqueKeyLoader,
    node: yaml.MappingNode,
    deep: bool = False,
) -> dict[Any, Any]:
    loader.flatten_mapping(node)
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as error:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "found an unhashable mapping key",
                key_node.start_mark,
            ) from error
        if duplicate:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    severity: str
    path: Path
    message: str

    def __str__(self) -> str:
        return f"{self.severity.upper()}: {self.path.as_posix()}: {self.message}"


@dataclass(frozen=True, slots=True)
class ValidationReport:
    document_count: int
    issues: tuple[ValidationIssue, ...]

    @property
    def errors(self) -> tuple[ValidationIssue, ...]:
        return tuple(issue for issue in self.issues if issue.severity == "error")

    @property
    def warnings(self) -> tuple[ValidationIssue, ...]:
        return tuple(issue for issue in self.issues if issue.severity == "warning")


def parse_front_matter(markdown: str) -> tuple[dict[str, Any], str]:
    """Return parsed front matter and Markdown body."""
    lines = markdown.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise FrontMatterError("canonical YAML front matter must start on line 1")

    closing_index = next(
        (index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"),
        None,
    )
    if closing_index is None:
        raise FrontMatterError("front matter closing delimiter is missing")

    raw_metadata = "".join(lines[1:closing_index])
    try:
        metadata = yaml.load(raw_metadata, Loader=UniqueKeyLoader)
    except yaml.YAMLError as error:
        raise FrontMatterError(f"invalid YAML: {error}") from error

    if not isinstance(metadata, dict):
        raise FrontMatterError("front matter must contain a YAML mapping")

    return metadata, "".join(lines[closing_index + 1 :])


def validate_document_metadata(metadata: dict[str, Any], path: Path) -> list[ValidationIssue]:
    """Validate one metadata mapping without repository-wide resolution."""
    issues: list[ValidationIssue] = []
    allowed_fields = set(REQUIRED_FIELDS) | set(OPTIONAL_FIELDS)

    for field in REQUIRED_FIELDS:
        if field not in metadata:
            issues.append(_error(path, f"missing required field '{field}'"))

    for field in metadata:
        if not isinstance(field, str):
            issues.append(_error(path, f"metadata key {field!r} must be a string"))
        elif field not in allowed_fields:
            issues.append(_error(path, f"unknown field '{field}'"))

    if metadata.get("metadata_schema") != SCHEMA_VERSION:
        issues.append(_error(path, f"metadata_schema must be '{SCHEMA_VERSION}'"))

    document_id = metadata.get("document_id")
    if not _matches(DOCUMENT_ID_PATTERN, document_id):
        issues.append(_error(path, "document_id has an invalid format"))
    else:
        filename_match = MANAGED_FILENAME_PATTERN.fullmatch(path.name)
        filename_document_id = filename_match.group("document_id") if filename_match else None
        if filename_document_id != document_id:
            issues.append(_error(path, "document_id does not match the filename"))

    canonical_id = metadata.get("canonical_id")
    if not _matches(CANONICAL_ID_PATTERN, canonical_id):
        issues.append(_error(path, "canonical_id has an invalid format"))
    elif isinstance(document_id, str) and canonical_id.split(".", 1)[0] != document_id.split("-", 1)[0].lower():
        issues.append(_error(path, "canonical_id library does not match document_id"))

    _validate_non_empty_string(metadata, "title", path, issues)
    _validate_non_empty_string(metadata, "owner", path, issues)

    if metadata.get("node_type") not in NODE_TYPES:
        issues.append(_error(path, "node_type is not supported"))
    if metadata.get("document_class") not in DOCUMENT_CLASSES:
        issues.append(_error(path, "document_class is not supported"))
    if not _matches(VERSION_PATTERN, metadata.get("version")):
        issues.append(_error(path, "version must be a SemVer value"))
    if metadata.get("status") not in STATUSES:
        issues.append(_error(path, "status is not supported"))
    elif metadata.get("status") == "canonical":
        if metadata.get("legacy_status") is not True:
            issues.append(_error(path, "status 'canonical' requires legacy_status: true"))
        else:
            issues.append(_warning(path, "status 'canonical' is legacy and requires governed migration"))
    elif "legacy_status" in metadata:
        issues.append(_error(path, "legacy_status is only valid with status 'canonical'"))
    if metadata.get("language") != "en":
        issues.append(_error(path, "language must be 'en' in metadata schema v1"))

    for field in ("domain", "discipline", "architecture_model"):
        if field in metadata:
            _validate_non_empty_string(metadata, field, path, issues)

    for field in ("authors", "reviewers", "applies_to", "tags", "aliases"):
        if field in metadata:
            _validate_string_list(metadata[field], field, path, issues)

    aliases = metadata.get("aliases", [])
    for alias in aliases if isinstance(aliases, list) else []:
        if not _matches(LEGACY_CANONICAL_ID_PATTERN, alias):
            issues.append(_error(path, f"alias '{alias}' has an invalid canonical ID format"))
        if alias == canonical_id:
            issues.append(_error(path, "an alias cannot equal canonical_id"))

    relationships = metadata.get("relationships", [])
    if not isinstance(relationships, list):
        issues.append(_error(path, "relationships must be a list"))
    else:
        for index, relationship in enumerate(relationships):
            _validate_relationship(relationship, index, path, issues)

    return issues


def validate_repository(
    root: Path,
    *,
    strict_placeholders: bool = False,
    sources: tuple[Path, ...] | None = None,
    is_excluded: Callable[[Path], bool] | None = None,
) -> ValidationReport:
    """Validate all identifier-bearing Markdown documents below root."""
    root = root.resolve()
    issues: list[ValidationIssue] = []
    documents: list[tuple[Path, dict[str, Any]]] = []

    for path in managed_documents(root, sources=sources, is_excluded=is_excluded):
        relative_path = path.relative_to(root)
        markdown = path.read_text(encoding="utf-8")
        if not markdown.strip():
            severity = "error" if strict_placeholders else "warning"
            issues.append(ValidationIssue(severity, relative_path, "empty placeholder is not a DEKG node"))
            continue

        try:
            metadata, _ = parse_front_matter(markdown)
        except FrontMatterError as error:
            issues.append(_error(relative_path, str(error)))
            continue

        issues.extend(validate_document_metadata(metadata, relative_path))
        documents.append((relative_path, metadata))

    issues.extend(_validate_repository_identity(documents))
    return ValidationReport(len(documents), tuple(issues))


def managed_documents(
    root: Path,
    *,
    sources: tuple[Path, ...] | None = None,
    is_excluded: Callable[[Path], bool] | None = None,
) -> Iterable[Path]:
    """Yield managed Markdown files in deterministic order."""
    resolved_root = root.resolve()
    search_roots = sources or (resolved_root,)
    documents: set[Path] = set()
    for search_root in search_roots:
        for path in search_root.rglob("*.md"):
            if path.is_symlink() or not path.is_file():
                continue
            resolved = path.resolve()
            if not resolved.is_relative_to(resolved_root):
                continue
            if is_excluded is not None and is_excluded(resolved):
                continue
            if MANAGED_FILENAME_PATTERN.fullmatch(path.name) is not None:
                documents.add(resolved)
    return iter(sorted(documents, key=lambda path: path.relative_to(resolved_root).as_posix()))


def _validate_repository_identity(documents: list[tuple[Path, dict[str, Any]]]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    document_ids: dict[str, Path] = {}
    canonical_ids: dict[str, Path] = {}
    aliases: dict[str, Path] = {}

    for path, metadata in documents:
        _record_unique(metadata.get("document_id"), path, "document_id", document_ids, issues)
        _record_unique(metadata.get("canonical_id"), path, "canonical_id", canonical_ids, issues)
        aliases_for_document = metadata.get("aliases", [])
        for alias in aliases_for_document if isinstance(aliases_for_document, list) else []:
            _record_unique(alias, path, "alias", aliases, issues)

    resolvable_ids = set(canonical_ids) | set(aliases)
    for alias, path in aliases.items():
        canonical_owner = canonical_ids.get(alias)
        if canonical_owner is not None:
            issues.append(
                _error(
                    path,
                    f"alias '{alias}' conflicts with a canonical_id used by {canonical_owner.as_posix()}",
                )
            )

    for path, metadata in documents:
        relationships = metadata.get("relationships", [])
        for relationship in relationships if isinstance(relationships, list) else []:
            if not isinstance(relationship, dict):
                continue
            target = relationship.get("target")
            if isinstance(target, str) and target not in resolvable_ids:
                issues.append(_error(path, f"relationship target '{target}' does not resolve"))
            if target == metadata.get("canonical_id"):
                issues.append(_error(path, "relationship cannot target its own document"))

    return issues


def _record_unique(
    value: Any,
    path: Path,
    field: str,
    registry: dict[str, Path],
    issues: list[ValidationIssue],
) -> None:
    if not isinstance(value, str):
        return
    previous = registry.get(value)
    if previous is not None:
        issues.append(_error(path, f"duplicate {field} '{value}' also used by {previous.as_posix()}"))
    else:
        registry[value] = path


def _validate_relationship(
    relationship: Any,
    index: int,
    path: Path,
    issues: list[ValidationIssue],
) -> None:
    label = f"relationships[{index}]"
    if not isinstance(relationship, dict):
        issues.append(_error(path, f"{label} must be a mapping"))
        return
    if set(relationship) != {"type", "target"}:
        issues.append(_error(path, f"{label} must contain only 'type' and 'target'"))
    if relationship.get("type") not in RELATIONSHIP_TYPES:
        issues.append(_error(path, f"{label}.type is not supported"))
    if not _matches(CANONICAL_ID_PATTERN, relationship.get("target")):
        issues.append(_error(path, f"{label}.target has an invalid canonical ID format"))


def _validate_non_empty_string(
    metadata: dict[str, Any],
    field: str,
    path: Path,
    issues: list[ValidationIssue],
) -> None:
    value = metadata.get(field)
    if not isinstance(value, str) or not value.strip():
        issues.append(_error(path, f"{field} must be a non-empty string"))


def _validate_string_list(value: Any, field: str, path: Path, issues: list[ValidationIssue]) -> None:
    if not isinstance(value, list) or not value:
        issues.append(_error(path, f"{field} must be a non-empty list"))
        return
    if any(not isinstance(item, str) or not item.strip() for item in value):
        issues.append(_error(path, f"{field} entries must be non-empty strings"))
    if len(value) != len({item for item in value if isinstance(item, str)}):
        issues.append(_error(path, f"{field} entries must be unique"))


def _matches(pattern: re.Pattern[str], value: Any) -> bool:
    return isinstance(value, str) and pattern.fullmatch(value) is not None


def _error(path: Path, message: str) -> ValidationIssue:
    return ValidationIssue("error", path, message)


def _warning(path: Path, message: str) -> ValidationIssue:
    return ValidationIssue("warning", path, message)
