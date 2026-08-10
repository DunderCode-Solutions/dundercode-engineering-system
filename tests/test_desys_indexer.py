from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path, PurePosixPath
from tempfile import TemporaryDirectory

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


class ConfigurationTests(unittest.TestCase):
    def test_loads_repository_configuration(self) -> None:
        config = load_config(Path("tools/desys_indexer.yaml"))

        self.assertEqual(config.repository_root, Path.cwd().resolve())
        self.assertEqual(config.artifacts, SUPPORTED_ARTIFACTS)
        self.assertIn(Path.cwd().resolve() / "foundation", config.sources)

    def test_rejects_output_path_traversal(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".git").mkdir()
            tools = root / "tools"
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

            with self.assertRaises(ConfigurationError):
                load_config(config_path)

    def test_rejects_source_path_traversal(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".git").mkdir()
            tools = root / "tools"
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

            with self.assertRaises(ConfigurationError):
                load_config(config_path)


class ScannerAndParserTests(unittest.TestCase):
    def test_scans_and_parses_real_corpus(self) -> None:
        config = load_config(Path("tools/desys_indexer.yaml"))

        paths = scan_markdown_documents(config)
        document = parse_document(paths[0], repository_root=config.repository_root)

        self.assertGreater(len(paths), 0)
        self.assertFalse(document.path.is_absolute())
        self.assertTrue(document.canonical_id)
        self.assertTrue(document.body.startswith("# "))

    def test_indexes_identifier_only_filename(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "knowledge"
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
                repository_root=root,
                sources=(source,),
                output_directory=root / "generated",
                exclude=(),
                artifacts=("index.yaml",),
            )

            paths = scan_markdown_documents(config)

        self.assertEqual([item.name for item in paths], ["DES-0200.md"])


class ArtifactTests(unittest.TestCase):
    def setUp(self) -> None:
        self.target = indexed_document(
            "knowledge/des/DES-0001-target.md",
            "DES-0001",
            "des.test.target",
            "Target",
            aliases=["des.legacy-target"],
        )
        self.source = indexed_document(
            "knowledge/dem/DEM-0001-source.md",
            "DEM-0001",
            "dem.test.source",
            "Source",
            relationships=[{"type": "depends_on", "target": "des.legacy-target"}],
        )

    def test_renders_all_artifacts_deterministically(self) -> None:
        first = render_indexes([self.source, self.target], SUPPORTED_ARTIFACTS)
        second = render_indexes([self.target, self.source], SUPPORTED_ARTIFACTS)

        self.assertEqual(first, second)
        self.assertEqual(set(first.files), set(SUPPORTED_ARTIFACTS))

        payloads = {
            name: json.loads(content) if name.endswith(".json") else yaml.safe_load(content)
            for name, content in first.files.items()
        }
        self.assertTrue(all(payload["build_id"] == first.build_id for payload in payloads.values()))
        self.assertEqual(
            payloads["graph.yaml"]["edges"],
            [
                {
                    "source": "dem.test.source",
                    "type": "depends_on",
                    "target": "des.test.target",
                }
            ],
        )
        self.assertEqual(
            payloads["aliases.yaml"]["aliases"],
            {"des.legacy-target": "des.test.target"},
        )
        search_target = next(
            document
            for document in payloads["search-index.json"]["documents"]
            if document["id"] == "des.test.target"
        )
        self.assertIn("applies_to", search_target)
        self.assertIn("discipline", search_target)
        self.assertIn("architecture_model", search_target)

    def test_writes_every_rendered_artifact(self) -> None:
        rendered = render_indexes([self.source, self.target], SUPPORTED_ARTIFACTS)

        with TemporaryDirectory() as directory:
            output = Path(directory) / "generated"
            write_indexes(rendered=rendered, output_dir=output)

            written = {path.name for path in output.iterdir()}
            self.assertEqual(written, set(SUPPORTED_ARTIFACTS))
            self.assertEqual((output / "index.yaml").read_text(encoding="utf-8"), rendered.files["index.yaml"])


class CommandTests(unittest.TestCase):
    def test_dry_run_succeeds(self) -> None:
        result = subprocess.run(
            [sys.executable, "-B", "tools/build_index.py", "--dry-run"],
            cwd=Path.cwd(),
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Validated and rendered", result.stdout)
        self.assertIn("documents", result.stdout)


if __name__ == "__main__":
    unittest.main()
