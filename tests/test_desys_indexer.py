from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path, PurePosixPath

import pytest
import yaml

from tools.desys_indexer.config import SUPPORTED_ARTIFACTS, ConfigurationError, load_config
from tools.desys_indexer.models import IndexedDocument
from tools.desys_indexer.parser import parse_document
from tools.desys_indexer.scanner import scan_markdown_documents
from tools.desys_indexer.writer import render_indexes, write_indexes


def metadata(
    document_id: str,
    canonical_id: str,
    title: str,
    *,
    aliases: list[str] | None = None,
    relationships: list[dict[str, str]] | None = None,
) -> dict[str, object]:
    result: dict[str, object] = {
        "metadata_schema": "1.0.0",
        "document_id": document_id,
        "canonical_id": canonical_id,
        "title": title,
        "node_type": "standard",
        "document_class": "normative",
        "version": "1.0.0",
        "status": "draft",
        "language": "en",
        "owner": "DunderCode Engineering",
    }
    if aliases:
        result["aliases"] = aliases
    if relationships:
        result["relationships"] = relationships
    return result


def indexed_document(
    path: str,
    document_id: str,
    canonical_id: str,
    title: str,
    *,
    aliases: list[str] | None = None,
    relationships: list[dict[str, str]] | None = None,
) -> IndexedDocument:
    return IndexedDocument(
        path=PurePosixPath(path),
        metadata=metadata(
            document_id,
            canonical_id,
            title,
            aliases=aliases,
            relationships=relationships,
        ),
        body=f"# {document_id} - {title}\n\nBody for {title}.\n",
        headings=(f"{document_id} - {title}",),
        summary=f"Body for {title}.",
    )


class TestConfiguration:
    def test_loads_repository_configuration(self) -> None:
        config = load_config(Path("tools/desys_indexer.yaml"))

        assert config.repository_root == Path.cwd().resolve()
        assert config.artifacts == SUPPORTED_ARTIFACTS
        assert Path.cwd().resolve() / "foundation" in config.sources

    def test_rejects_output_path_traversal(self, tmp_path: Path) -> None:
        (tmp_path / ".git").mkdir()
        tools = tmp_path / "tools"
        tools.mkdir()
        config_path = tools / "indexer.yaml"
        config_path.write_text(
            """version: 1
repository_root: ..
sources: [tools]
output_directory: ../outside
exclude: [.git]
artifacts: [index.yaml]
""",
            encoding="utf-8",
        )

        with pytest.raises(ConfigurationError):
            load_config(config_path)

    def test_rejects_source_path_traversal(self, tmp_path: Path) -> None:
        (tmp_path / ".git").mkdir()
        tools = tmp_path / "tools"
        tools.mkdir()
        config_path = tools / "indexer.yaml"
        config_path.write_text(
            """version: 1
repository_root: ..
sources: [tools/../tools]
output_directory: generated
exclude: [.git]
artifacts: [index.yaml]
""",
            encoding="utf-8",
        )

        with pytest.raises(ConfigurationError):
            load_config(config_path)


class TestScannerAndParser:
    def test_scans_and_parses_real_corpus(self) -> None:
        config = load_config(Path("tools/desys_indexer.yaml"))

        paths = scan_markdown_documents(config)
        document = parse_document(paths[0], repository_root=config.repository_root)

        assert len(paths) > 0
        assert not document.path.is_absolute()
        assert document.canonical_id
        assert document.body.startswith("# ")

    def test_indexes_identifier_only_filename(self, tmp_path: Path) -> None:
        source = tmp_path / "knowledge"
        source.mkdir()
        path = source / "DES-0200.md"
        metadata_text = yaml.safe_dump(
            metadata("DES-0200", "des.quality.code-quality", "Code Quality"),
            sort_keys=False,
        ).rstrip()
        path.write_text(
            f"---\n{metadata_text}\n---\n\n# DES-0200 - Code Quality\n\nBody.\n",
            encoding="utf-8",
        )
        from tools.desys_indexer.config import IndexerConfig

        config = IndexerConfig(
            version=1,
            repository_root=tmp_path,
            sources=(source,),
            output_directory=tmp_path / "generated",
            exclude=(),
            artifacts=("index.yaml",),
        )

        paths = scan_markdown_documents(config)

        assert [item.name for item in paths] == ["DES-0200.md"]


@pytest.fixture
def artifact_documents() -> tuple[IndexedDocument, IndexedDocument]:
    target = indexed_document(
        "knowledge/des/DES-0001-target.md",
        "DES-0001",
        "des.test.target",
        "Target",
        aliases=["des.legacy-target"],
    )
    source = indexed_document(
        "knowledge/dem/DEM-0001-source.md",
        "DEM-0001",
        "dem.test.source",
        "Source",
        relationships=[{"type": "depends_on", "target": "des.legacy-target"}],
    )
    return source, target


class TestArtifacts:
    def test_renders_all_artifacts_deterministically(
        self,
        artifact_documents: tuple[IndexedDocument, IndexedDocument],
    ) -> None:
        source, target = artifact_documents
        first = render_indexes([source, target], SUPPORTED_ARTIFACTS)
        second = render_indexes([target, source], SUPPORTED_ARTIFACTS)

        assert first == second
        assert set(first.files) == set(SUPPORTED_ARTIFACTS)

        payloads = {
            name: json.loads(content) if name.endswith(".json") else yaml.safe_load(content)
            for name, content in first.files.items()
        }
        assert all(payload["build_id"] == first.build_id for payload in payloads.values())
        assert payloads["graph.yaml"]["edges"] == [
            {
                "source": "dem.test.source",
                "type": "depends_on",
                "target": "des.test.target",
            }
        ]
        assert payloads["aliases.yaml"]["aliases"] == {
            "des.legacy-target": "des.test.target"
        }
        search_target = next(
            document
            for document in payloads["search-index.json"]["documents"]
            if document["id"] == "des.test.target"
        )
        assert "applies_to" in search_target
        assert "discipline" in search_target
        assert "architecture_model" in search_target

    def test_writes_every_rendered_artifact(
        self,
        artifact_documents: tuple[IndexedDocument, IndexedDocument],
        tmp_path: Path,
    ) -> None:
        source, target = artifact_documents
        rendered = render_indexes([source, target], SUPPORTED_ARTIFACTS)

        output = tmp_path / "generated"
        write_indexes(rendered=rendered, output_dir=output)

        written = {path.name for path in output.iterdir()}
        assert written == set(SUPPORTED_ARTIFACTS)
        assert (output / "index.yaml").read_text(encoding="utf-8") == rendered.files["index.yaml"]


class TestCommand:
    def test_dry_run_succeeds(self) -> None:
        result = subprocess.run(
            [sys.executable, "-B", "tools/build_index.py", "--dry-run"],
            cwd=Path.cwd(),
            check=False,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, result.stderr
        assert "Validated and rendered" in result.stdout
        assert "documents" in result.stdout
