"""
DESys Indexer Configuration

Loads and validates the DESys Indexer configuration.

Author:
    DunderCode Engineering
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

SUPPORTED_SCHEMA_VERSION = 1


class ConfigurationError(Exception):
    """Raised when the indexer configuration is invalid."""


@dataclass(slots=True, frozen=True)
class IndexerConfig:
    """
    DESys Indexer configuration model.
    """

    version: int

    repository_root: Path

    sources: tuple[Path, ...]

    output_directory: Path

    exclude: tuple[str, ...]

    artifacts: tuple[str, ...]

    @property
    def generated_directory(self) -> Path:
        """Returns the generated artifacts directory."""
        return self.output_directory

    def is_excluded(self, directory: str) -> bool:
        """Checks whether a directory should be ignored."""
        return directory in self.exclude


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def load_config(path: Path) -> IndexerConfig:
    """
    Load and validate the DESys Indexer configuration.

    Parameters
    ----------
    path:
        Configuration file.

    Returns
    -------
    IndexerConfig

    Raises
    ------
    FileNotFoundError
    ConfigurationError
    """

    path = path.resolve()

    if not path.exists():
        raise FileNotFoundError(path)

    with path.open(
        "r",
        encoding="utf-8",
    ) as stream:
        data = yaml.safe_load(stream)

    if data is None:
        raise ConfigurationError(
            "Configuration file is empty."
        )

    return _build_config(
        data=data,
        config_directory=path.parent,
    )


# ---------------------------------------------------------------------
# Internal
# ---------------------------------------------------------------------


def _build_config(
    *,
    data: dict[str, Any],
    config_directory: Path,
) -> IndexerConfig:
    """
    Convert raw YAML into a validated configuration object.
    """

    required = (
        "version",
        "repository_root",
        "sources",
        "output_directory",
        "exclude",
        "artifacts",
    )

    for key in required:
        _require(data, key)

    version = int(data["version"])

    if version != SUPPORTED_SCHEMA_VERSION:
        raise ConfigurationError(
            f"Unsupported schema version: {version}"
        )

    repository_root = (
        config_directory / data["repository_root"]
    ).resolve()

    sources = tuple(
        (repository_root / source).resolve()
        for source in data["sources"]
    )

    output_directory = (
        repository_root / data["output_directory"]
    ).resolve()

    exclude = tuple(str(item) for item in data["exclude"])

    artifacts = tuple(str(item) for item in data["artifacts"])

    return IndexerConfig(
        version=version,
        repository_root=repository_root,
        sources=sources,
        output_directory=output_directory,
        exclude=exclude,
        artifacts=artifacts,
    )


def _require(
    data: dict[str, Any],
    key: str,
) -> None:
    """
    Validate required configuration keys.
    """

    if key not in data:
        raise ConfigurationError(
            f"Missing configuration key '{key}'."
        )