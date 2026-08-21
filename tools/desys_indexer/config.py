"""Configuration loading and path validation for the DESys indexer."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

from tools.desys_metadata import UniqueKeyLoader

SUPPORTED_SCHEMA_VERSION = 1
SUPPORTED_ARTIFACTS = (
    "index.yaml",
    "graph.yaml",
    "navigation.yaml",
    "aliases.yaml",
    "search-index.json",
)


class ConfigurationError(ValueError):
    """Raised when indexer configuration is invalid or unsafe."""


@dataclass(frozen=True, slots=True)
class IndexerConfig:
    version: int
    repository_root: Path
    sources: tuple[Path, ...]
    output_directory: Path
    exclude: tuple[str, ...]
    artifacts: tuple[str, ...]

    def is_excluded(self, path: Path) -> bool:
        """Return whether a repository path matches an exclusion rule."""
        relative = path.resolve().relative_to(self.repository_root)
        relative_posix = PurePosixPath(relative.as_posix())
        for rule in self.exclude:
            rule_path = PurePosixPath(rule)
            if len(rule_path.parts) == 1:
                if rule in relative_posix.parts:
                    return True
            elif relative_posix == rule_path or rule_path in relative_posix.parents:
                return True
        return False


def load_config(path: Path) -> IndexerConfig:
    """Load and validate an indexer YAML configuration."""
    path = path.resolve()
    if not path.is_file():
        raise FileNotFoundError(path)

    try:
        data = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    except yaml.YAMLError as error:
        raise ConfigurationError(f"Invalid configuration YAML: {error}") from error
    if not isinstance(data, dict):
        raise ConfigurationError("Configuration must be a YAML mapping.")

    return _build_config(data, path.parent)


def _build_config(data: dict[str, Any], config_directory: Path) -> IndexerConfig:
    required = {"version", "repository_root", "sources", "output_directory", "exclude", "artifacts"}
    missing = sorted(required - set(data))
    unknown = sorted(set(data) - required)
    if missing:
        raise ConfigurationError(f"Missing configuration field(s): {', '.join(missing)}")
    if unknown:
        raise ConfigurationError(f"Unknown configuration field(s): {', '.join(unknown)}")

    if data["version"] != SUPPORTED_SCHEMA_VERSION:
        raise ConfigurationError(f"Unsupported configuration version: {data['version']!r}")

    repository_value = _require_relative_path(data["repository_root"], "repository_root", allow_parent=True)
    repository_root = (config_directory / repository_value).resolve()
    if not repository_root.is_dir():
        raise ConfigurationError(f"Repository root is not a directory: {repository_root}")
    if not config_directory.resolve().is_relative_to(repository_root):
        raise ConfigurationError("Configuration file must be located inside repository_root.")
    if not (repository_root / ".git").exists():
        raise ConfigurationError("repository_root must contain a Git worktree.")

    source_values = [
        _require_relative_path(value, "source")
        for value in _require_string_list(data["sources"], "sources")
    ]
    sources = tuple(
        _resolve_inside_root(repository_root, value, "source", require_directory=True)
        for value in source_values
    )
    if len(sources) != len(set(sources)):
        raise ConfigurationError("Source directories must be unique.")

    output_value = _require_relative_path(data["output_directory"], "output_directory")
    output_directory = _resolve_inside_root(repository_root, output_value, "output_directory")

    excludes = tuple(_normalize_repository_path(value, "exclude") for value in _require_string_list(data["exclude"], "exclude"))
    if len(excludes) != len(set(excludes)):
        raise ConfigurationError("Exclude rules must be unique.")

    artifacts = tuple(_require_string_list(data["artifacts"], "artifacts"))
    if len(artifacts) != len(set(artifacts)):
        raise ConfigurationError("Artifacts must be unique.")
    unsupported = sorted(set(artifacts) - set(SUPPORTED_ARTIFACTS))
    if unsupported:
        raise ConfigurationError(f"Unsupported artifact(s): {', '.join(unsupported)}")
    if not artifacts:
        raise ConfigurationError("At least one artifact is required.")

    return IndexerConfig(
        version=SUPPORTED_SCHEMA_VERSION,
        repository_root=repository_root,
        sources=sources,
        output_directory=output_directory,
        exclude=excludes,
        artifacts=artifacts,
    )


def _require_string_list(value: Any, field: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ConfigurationError(f"{field} must be a non-empty list.")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise ConfigurationError(f"{field} entries must be non-empty strings.")
    return value


def _require_relative_path(value: Any, field: str, *, allow_parent: bool = False) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ConfigurationError(f"{field} must be a non-empty path string.")
    path = PurePosixPath(value)
    if path.is_absolute():
        raise ConfigurationError(f"{field} must be relative.")
    if not allow_parent and ".." in path.parts:
        raise ConfigurationError(f"{field} must not contain '..'.")
    return value


def _normalize_repository_path(value: str, field: str) -> str:
    normalized = _require_relative_path(value, field)
    return PurePosixPath(normalized).as_posix().rstrip("/")


def _resolve_inside_root(
    root: Path,
    value: str,
    field: str,
    *,
    require_directory: bool = False,
) -> Path:
    resolved = (root / value).resolve()
    if not resolved.is_relative_to(root):
        raise ConfigurationError(f"{field} resolves outside repository root: {value}")
    if require_directory and not resolved.is_dir():
        raise ConfigurationError(f"{field} is not a directory: {value}")
    return resolved
