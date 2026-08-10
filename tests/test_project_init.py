from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from tools.check_generated_artifacts import validate_generated_artifacts
from tools.desys_indexer.config import SUPPORTED_ARTIFACTS, load_config
from tools.desys_indexer.parser import parse_documents
from tools.desys_indexer.scanner import scan_markdown_documents
from tools.desys_indexer.writer import render_indexes, write_indexes
from tools.init_project import ProjectInitializationError, initialize_project


def make_repository(directory: Path) -> Path:
    directory.mkdir()
    subprocess.run(
        ["git", "init", "--quiet", str(directory)],
        check=True,
        capture_output=True,
        text=True,
    )
    return directory


def test_dry_run_reports_plan_without_writing(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")

    plan = initialize_project(root, dry_run=True, version="0.1.0")

    assert not plan.has_conflicts
    assert all(operation.action == "CREATE" for operation in plan.operations)
    assert [path.name for path in root.iterdir()] == [".git"]


def test_initializes_a_loadable_consumer_configuration(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")

    first = initialize_project(root, version="0.1.0")
    config = load_config(root / "tools/desys_indexer.yaml")

    assert not first.has_conflicts
    assert config.repository_root == root.resolve()
    assert config.artifacts == SUPPORTED_ARTIFACTS
    assert {path.relative_to(root.resolve()).as_posix() for path in config.sources} == {
        "docs/adr",
        "docs/prd",
        "docs/rfc",
    }
    assert "/docs/generated/" in (root / ".gitignore").read_text(encoding="utf-8")

    documents = parse_documents(
        scan_markdown_documents(config), repository_root=config.repository_root
    )
    rendered = render_indexes(documents, config.artifacts)
    write_indexes(rendered=rendered, output_dir=config.output_directory)
    summary = validate_generated_artifacts(config.output_directory)

    assert summary["document_count"] == 0
    assert summary["artifact_count"] == 5
    quality_script = (root / "scripts/desys-docs-quality.sh").read_text(encoding="utf-8")
    assert '${BASH_SOURCE[0]}' in quality_script
    agents = (root / "AGENTS.md").read_text(encoding="utf-8")
    assert "docs/generated/search-index.json" in agents
    assert "source Markdown is authoritative" in agents


def test_second_run_is_idempotent(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    initialize_project(root, version="0.1.0")
    files = tuple(
        path for path in root.rglob("*") if path.is_file() and ".git" not in path.parts
    )
    before = {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in files}

    plan = initialize_project(root, version="0.1.0")

    assert not plan.has_conflicts
    assert all(operation.action == "UNCHANGED" for operation in plan.operations)
    assert {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in files} == before


def test_conflict_prevents_all_writes(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    tools = root / "tools"
    tools.mkdir()
    config = tools / "desys_indexer.yaml"
    config.write_text("consumer-owned: true\n", encoding="utf-8")

    plan = initialize_project(root, version="0.1.0")

    assert plan.has_conflicts
    assert config.read_text(encoding="utf-8") == "consumer-owned: true\n"
    assert not (root / "docs").exists()
    assert not (root / ".gitignore").exists()


def test_extends_existing_gitignore_once(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    gitignore = root / ".gitignore"
    gitignore.write_text(".venv/\n", encoding="utf-8")

    first = initialize_project(root, version="0.1.0")
    second = initialize_project(root, version="0.1.0")
    content = gitignore.read_text(encoding="utf-8")

    assert "UPDATE" in {operation.action for operation in first.operations}
    assert not second.has_conflicts
    assert content.count("/docs/generated/") == 1
    assert content.startswith(".venv/\n\n")


def test_extends_existing_agents_file_once(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    agents = root / "AGENTS.md"
    agents.write_text("# Existing Agent Instructions\n", encoding="utf-8")

    first = initialize_project(root, version="0.1.0")
    second = initialize_project(root, version="0.1.0")
    content = agents.read_text(encoding="utf-8")

    agents_operation = next(operation for operation in first.operations if operation.path.as_posix() == "AGENTS.md")
    assert agents_operation.action == "UPDATE"
    assert not second.has_conflicts
    assert content.startswith("# Existing Agent Instructions\n\n")
    assert content.count("<!-- BEGIN DESys documentation instructions -->") == 1
    assert content.count("<!-- END DESys documentation instructions -->") == 1


def test_rejects_malformed_agents_markers_without_writing(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    agents = root / "AGENTS.md"
    original = "<!-- BEGIN DESys documentation instructions -->\nIncomplete\n"
    agents.write_text(original, encoding="utf-8")

    plan = initialize_project(root, version="0.1.0")

    assert plan.has_conflicts
    assert agents.read_text(encoding="utf-8") == original
    assert not (root / "docs").exists()


def test_rejects_non_git_root(tmp_path: Path) -> None:
    with pytest.raises(ProjectInitializationError):
        initialize_project(tmp_path, dry_run=True, version="0.1.0")


def test_cli_returns_failure_for_non_git_root(tmp_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "tools.init_project", "--root", str(tmp_path), "--dry-run"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "must contain a non-symlinked .git entry" in result.stderr


def test_rejects_symlinked_managed_path(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    external = tmp_path / "external"
    external.mkdir()
    (root / "docs").symlink_to(external, target_is_directory=True)

    plan = initialize_project(root, version="0.1.0")

    assert plan.has_conflicts
    assert not (root / "tools").exists()
