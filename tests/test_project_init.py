from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path, PurePosixPath

import pytest
import yaml

from tools import init_project as init_project_module
from tools.check_generated_artifacts import validate_generated_artifacts
from tools.corpus_resources import (
    BundleEntry,
    ConsumerManifest,
    DescriptorEntry,
    PredecessorDescriptor,
    ReferenceBundle,
    load_predecessor_descriptor,
    load_reference_bundle,
    render_consumer_manifest,
)
from tools.desys_indexer.config import SUPPORTED_ARTIFACTS, load_config
from tools.desys_indexer.parser import parse_documents
from tools.desys_indexer.scanner import scan_markdown_documents
from tools.desys_indexer.writer import render_indexes, write_indexes
from tools.desys_metadata import validate_repository
from tools.init_project import ProjectInitializationError, initialize_project

TEST_VERSION = "0.3.0a1"
V02_BUNDLE_CHECKSUM = "sha256:d78bb3a685bf285f29d542d1709be9874842f759f00d9739ba073ce94633f62a"


def make_repository(directory: Path) -> Path:
    directory.mkdir()
    subprocess.run(
        ["git", "init", "--quiet", str(directory)],
        check=True,
        capture_output=True,
        text=True,
    )
    return directory


def write_v02_predecessor_manifest(root: Path) -> Path:
    descriptor = load_predecessor_descriptor(V02_BUNDLE_CHECKSUM)
    payload = {
        "manifest_schema": "1.1.0",
        "package_name": "dundercode-engineering-system",
        "package_version": "0.2.0a1",
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
    path = root / "docs/desys/corpus-manifest.yaml"
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    return path


def test_dry_run_reports_plan_without_writing(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")

    plan = initialize_project(root, dry_run=True, version=TEST_VERSION)

    assert not plan.has_conflicts
    assert all(operation.action == "CREATE" for operation in plan.operations)
    assert [path.name for path in root.iterdir()] == [".git"]


def test_default_initialization_does_not_install_reference_corpus(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")

    initialize_project(root, version=TEST_VERSION)

    assert not (root / "docs/desys/corpus-manifest.yaml").exists()
    assert not (root / "docs/desys/reference").exists()
    assert (root / "tools/desys_indexer.yaml").read_text(encoding="utf-8").count("docs/desys/reference") == 0


def test_reference_corpus_dry_run_plans_without_writing(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")

    plan = initialize_project(root, dry_run=True, version=TEST_VERSION, with_reference_corpus=True)

    corpus_files = [
        operation
        for operation in plan.operations
        if operation.path.as_posix() == "docs/desys/corpus-manifest.yaml"
        or "docs/desys/reference" in operation.path.as_posix()
        or operation.path.name in {"LICENSE", "THIRD_PARTY_NOTICES.md"}
    ]
    assert not plan.has_conflicts
    assert corpus_files
    assert all(operation.action == "CREATE" for operation in corpus_files)
    assert [path.name for path in root.iterdir()] == [".git"]


def test_reference_corpus_dry_run_matches_applied_plan(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")

    planned = initialize_project(root, dry_run=True, version=TEST_VERSION, with_reference_corpus=True)
    applied = initialize_project(root, version=TEST_VERSION, with_reference_corpus=True)

    assert planned == applied


def test_initializes_a_loadable_consumer_configuration(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")

    first = initialize_project(root, version=TEST_VERSION)
    config = load_config(root / "tools/desys_indexer.yaml")

    assert not first.has_conflicts
    assert config.repository_root == root.resolve()
    assert config.artifacts == SUPPORTED_ARTIFACTS
    assert {path.relative_to(root.resolve()).as_posix() for path in config.sources} == {
        "docs/adr",
        "docs/prd",
        "docs/rfc",
    }
    gitignore = (root / ".gitignore").read_text(encoding="utf-8")
    assert "/docs/generated/" in gitignore
    assert "Regenerated by scripts/desys-docs-quality.sh" in gitignore
    assert (root / "tools/desys-source.txt").read_text(encoding="utf-8") == (
        "dundercode-engineering-system==0.3.0a1\n"
    )

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
    assert "uvx --isolated --no-config --python 3.12" in quality_script
    assert "uv sync" not in quality_script
    workflow = (root / ".github/workflows/desys-docs-quality.yml").read_text(encoding="utf-8")
    assert "actions/setup-python" not in workflow
    assert "cache-dependency-glob: tools/desys-source.txt" in workflow
    assert "  push:\n" in workflow
    assert "    branches:\n" not in workflow
    agents = (root / "AGENTS.md").read_text(encoding="utf-8")
    assert "docs/generated/search-index.json" in agents
    assert "source Markdown is authoritative" in agents
    assert "Cite repository-relative paths" in agents
    assert "source --relationship--> target" in agents
    assert "`draft`, `review`, `approved`, `published`,\nand `deprecated`" in agents
    assert "`legacy_status: true`" in agents
    assert "Neither field alone establishes whether a document is binding" in agents
    assert "Determine authority from explicit project\ngovernance evidence" in agents
    assert "does not imply unilateral approval\npower" in agents
    assert "do not define a required transition sequence" in agents
    assert "approval process, or mandatory artifact type" in agents
    assert "optional proposals that\nrequire confirmation" in agents
    assert "only when the documented project process or requested task requires" in agents
    assert "require explicit confirmation" in agents
    assert "cannot make them authoritative" in agents
    assert "Metadata schema v1 requires `language: en`" in agents
    assert "write source document prose in\n   English" in agents
    assert "Do not label non-English content as `en`" in agents
    assert "`approved` and `published` documents govern" not in agents


def test_second_run_is_idempotent(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    initialize_project(root, version=TEST_VERSION)
    files = tuple(
        path for path in root.rglob("*") if path.is_file() and ".git" not in path.parts
    )
    before = {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in files}

    plan = initialize_project(root, version=TEST_VERSION)

    assert not plan.has_conflicts
    assert all(operation.action == "UNCHANGED" for operation in plan.operations)
    assert {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in files} == before


def test_installs_reference_corpus_manifest_legal_files_and_sources(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    vendor = root / "tools/vendor"
    vendor.mkdir(parents=True)
    wheel = vendor / "dundercode_engineering_system-0.3.0a1-py3-none-any.whl"
    wheel.write_bytes(b"pilot wheel")
    source = wheel.relative_to(root).as_posix()

    plan = initialize_project(
        root,
        version=TEST_VERSION,
        desys_source=source,
        with_reference_corpus=True,
    )
    bundle = load_reference_bundle()
    manifest = yaml.safe_load((root / "docs/desys/corpus-manifest.yaml").read_text(encoding="utf-8"))
    config = load_config(root / "tools/desys_indexer.yaml")

    assert not plan.has_conflicts
    assert manifest["manifest_schema"] == "1.1.0"
    assert manifest["package_version"] == TEST_VERSION
    assert manifest["package_source"] == source
    assert manifest["release_tag"] == bundle.release_tag == "v0.3.0-alpha.1"
    assert manifest["source_commit"] == bundle.source_commit == "d84693cd117e5b792fe63fcaaa1550acda427c16"
    assert manifest["corpus_version"] == bundle.corpus_version
    assert manifest["bundle_checksum"] == bundle.bundle_checksum
    assert len(manifest["entries"]) == 41
    assert {entry["classification"] for entry in manifest["entries"]} >= {"document", "navigation", "legal"}
    assert all(entry["distribution"] == "approved" for entry in manifest["entries"])
    assert all(entry["original_checksum"] == entry["installed_checksum"] for entry in manifest["entries"])
    assert (root / "docs/desys/LICENSE").read_bytes() == next(
        entry.content for entry in bundle.entries if entry.target.as_posix() == "docs/desys/LICENSE"
    )
    assert (root / "docs/desys/THIRD_PARTY_NOTICES.md").is_file()
    assert all((root / entry.target).stat().st_mode & 0o111 == 0 for entry in bundle.entries)
    assert {path.relative_to(root).as_posix() for path in config.sources} == {
        "docs/adr",
        "docs/prd",
        "docs/rfc",
        "docs/desys/reference/delivery",
        "docs/desys/reference/engineering",
        "docs/desys/reference/foundation",
        "docs/desys/reference/knowledge",
    }
    readme = (root / "docs/desys/README.md").read_text(encoding="utf-8")
    assert "reference-only" in readme
    assert "ownership boundary" in readme
    agents = (root / "AGENTS.md").read_text(encoding="utf-8")
    assert "They do not override consumer code, policies, ADRs, PRDs, RFCs" in agents
    assert "Report contradictions and follow the consumer project's evidence" in agents
    assert "defines DESys ownership of vendored files" in agents
    assert "generated indexes as ownership or authority evidence" in agents


def test_opt_in_preserves_consumer_owned_documents(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    initialize_project(root, version=TEST_VERSION)
    consumer_files = {
        root / "docs/adr/ADR-0042-consumer.md": b"consumer adr\n",
        root / "docs/prd/PRD-0042-consumer.md": b"consumer prd\n",
        root / "docs/rfc/RFC-0042-consumer.md": b"consumer rfc\n",
    }
    for path, content in consumer_files.items():
        path.write_bytes(content)

    plan = initialize_project(root, version=TEST_VERSION, with_reference_corpus=True)

    assert not plan.has_conflicts
    assert {path: path.read_bytes() for path in consumer_files} == consumer_files


def test_opt_in_rejects_unmanaged_paths_inside_reference_namespace(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    initialize_project(root, version=TEST_VERSION)
    unmanaged = root / "docs/desys/reference/consumer.md"
    unmanaged.parent.mkdir(parents=True)
    unmanaged.write_bytes(b"consumer owned\n")
    managed = (root / "AGENTS.md", root / "docs/desys/README.md", root / "tools/desys_indexer.yaml")
    before = {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in managed}

    plan = initialize_project(root, version=TEST_VERSION, with_reference_corpus=True)

    conflict = next(
        operation
        for operation in plan.operations
        if operation.path.as_posix() == unmanaged.relative_to(root).as_posix()
    )
    assert plan.has_conflicts
    assert conflict.reason == "unmanaged path inside the DESys reference namespace"
    assert unmanaged.read_bytes() == b"consumer owned\n"
    assert {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in managed} == before
    assert not (root / "docs/desys/corpus-manifest.yaml").exists()


def test_metadata_validation_reports_consumer_corpus_identity_collision(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    initialize_project(root, version=TEST_VERSION, with_reference_corpus=True)
    consumer = root / "docs/rfc/RFC-0042-consumer.md"
    consumer.write_text(
        """---
metadata_schema: 1.0.0
document_id: RFC-0042
canonical_id: rfc.corpus.reference-distribution
title: Consumer RFC
node_type: proposal
document_class: normative
version: 1.0.0
status: draft
language: en
owner: Consumer
---
# Consumer RFC
""",
        encoding="utf-8",
    )
    config = load_config(root / "tools/desys_indexer.yaml")

    report = validate_repository(root, sources=config.sources, is_excluded=config.is_excluded)

    collision = next(issue for issue in report.errors if "duplicate canonical_id" in issue.message)
    assert collision.path == Path("docs/rfc/RFC-0042-consumer.md")
    assert "docs/desys/reference/knowledge/rfc/RFC-0001-reference-corpus-distribution.md" in collision.message


def test_reference_corpus_rerun_preserves_bytes_and_mtimes(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    initialize_project(root, version=TEST_VERSION, with_reference_corpus=True)
    files = tuple(
        path for path in (root / "docs/desys").rglob("*") if path.is_file()
    )
    before = {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in files}
    time.sleep(0.01)

    plan = initialize_project(root, version=TEST_VERSION, with_reference_corpus=True)

    corpus_operations = [
        operation
        for operation in plan.operations
        if operation.path.as_posix() == "docs/desys/corpus-manifest.yaml"
        or operation.path.as_posix().startswith("docs/desys/reference/")
        or operation.path.name in {"LICENSE", "THIRD_PARTY_NOTICES.md"}
    ]
    assert not plan.has_conflicts
    assert all(operation.action == "UNCHANGED" for operation in corpus_operations)
    assert {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in files} == before


@pytest.mark.parametrize("change", ["modify", "delete"])
@pytest.mark.parametrize("with_reference_corpus", [False, True])
def test_local_corpus_change_conflicts_without_other_writes(
    tmp_path: Path,
    change: str,
    with_reference_corpus: bool,
) -> None:
    root = make_repository(tmp_path / "repository")
    initialize_project(root, version=TEST_VERSION, with_reference_corpus=True)
    bundle = load_reference_bundle()
    changed = root / bundle.entries[-1].target
    sentinel = root / bundle.entries[0].target
    sentinel_before = (sentinel.read_bytes(), sentinel.stat().st_mtime_ns)
    manifest = root / "docs/desys/corpus-manifest.yaml"
    manifest_before = (manifest.read_bytes(), manifest.stat().st_mtime_ns)
    if change == "modify":
        changed.write_bytes(changed.read_bytes() + b"\nlocal change\n")
    else:
        changed.unlink()

    plan = initialize_project(root, version=TEST_VERSION, with_reference_corpus=with_reference_corpus)

    operation = next(item for item in plan.operations if item.path == bundle.entries[-1].target)
    assert plan.has_conflicts
    assert operation.action == "CONFLICT"
    assert sentinel_before == (sentinel.read_bytes(), sentinel.stat().st_mtime_ns)
    assert manifest_before == (manifest.read_bytes(), manifest.stat().st_mtime_ns)


def test_unmanaged_corpus_target_blocks_first_install(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    target = root / "docs/desys/LICENSE"
    target.parent.mkdir(parents=True)
    target.write_text("consumer owned\n", encoding="utf-8")

    plan = initialize_project(root, version=TEST_VERSION, with_reference_corpus=True)

    assert plan.has_conflicts
    assert target.read_text(encoding="utf-8") == "consumer owned\n"
    assert not (root / "docs/desys/corpus-manifest.yaml").exists()
    assert not (root / "tools").exists()


def test_malformed_corpus_manifest_blocks_all_writes(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    initialize_project(root, version=TEST_VERSION, with_reference_corpus=True)
    manifest = root / "docs/desys/corpus-manifest.yaml"
    manifest.write_text("manifest_schema: 1.1.0\nmanifest_schema: duplicate\n", encoding="utf-8")
    readme = root / "docs/desys/README.md"
    before = (readme.read_bytes(), readme.stat().st_mtime_ns)

    plan = initialize_project(root, version=TEST_VERSION, with_reference_corpus=True)

    assert plan.has_conflicts
    assert next(
        item
        for item in plan.operations
        if item.path.as_posix() == "docs/desys/corpus-manifest.yaml"
    ).action == "CONFLICT"
    assert before == (readme.read_bytes(), readme.stat().st_mtime_ns)


def test_omitted_flag_rejects_unowned_manifest_without_enabling_corpus(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    initialize_project(root, version=TEST_VERSION)
    manifest = root / "docs/desys/corpus-manifest.yaml"
    manifest.write_text("not: a corpus manifest\n", encoding="utf-8")
    agents = root / "AGENTS.md"
    config = root / "tools/desys_indexer.yaml"
    before = {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in (agents, config)}

    plan = initialize_project(root, version=TEST_VERSION)

    assert plan.has_conflicts
    assert next(
        item
        for item in plan.operations
        if item.path.as_posix() == "docs/desys/corpus-manifest.yaml"
    ).action == "CONFLICT"
    assert {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in (agents, config)} == before
    assert "docs/desys/reference" not in config.read_text(encoding="utf-8")


def test_omitted_flag_rejects_unsupported_manifest_without_enabling_corpus(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    initialize_project(root, version=TEST_VERSION)
    bundle = load_reference_bundle()
    manifest = yaml.safe_load(
        render_consumer_manifest(
            bundle,
            package_name="dundercode-engineering-system",
            package_version=TEST_VERSION,
            package_source=f"dundercode-engineering-system=={TEST_VERSION}",
        )
    )
    manifest["bundle_checksum"] = f"sha256:{'f' * 64}"
    manifest_path = root / "docs/desys/corpus-manifest.yaml"
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    managed = (
        root / "AGENTS.md",
        root / "docs/desys/README.md",
        root / "tools/desys_indexer.yaml",
    )
    before = {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in managed}

    plan = initialize_project(root, version=TEST_VERSION)

    manifest_operation = next(
        item
        for item in plan.operations
        if item.path.as_posix() == "docs/desys/corpus-manifest.yaml"
    )
    assert plan.has_conflicts
    assert manifest_operation.reason == "unsupported prior corpus bundle"
    assert {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in managed} == before
    assert "docs/desys/reference" not in (root / "tools/desys_indexer.yaml").read_text(encoding="utf-8")


@pytest.mark.parametrize(
    ("field", "value", "reason"),
    (
        (
            "release_tag",
            "v0.2.0-beta.1",
            "invalid corpus ownership manifest: release_tag does not match package_version.",
        ),
        ("source_commit", "a" * 40, "corpus manifest release provenance is inconsistent"),
    ),
)
def test_rejects_inconsistent_release_provenance_without_writing(
    tmp_path: Path,
    field: str,
    value: str,
    reason: str,
) -> None:
    root = make_repository(tmp_path / "repository")
    initialize_project(root, version=TEST_VERSION, with_reference_corpus=True)
    manifest_path = root / "docs/desys/corpus-manifest.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest[field] = value
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    readme = root / "docs/desys/README.md"
    before = (readme.read_bytes(), readme.stat().st_mtime_ns)

    plan = initialize_project(root, version=TEST_VERSION, with_reference_corpus=True)

    operation = next(
        item
        for item in plan.operations
        if item.path.as_posix() == "docs/desys/corpus-manifest.yaml"
    )
    assert plan.has_conflicts
    assert operation.reason == reason
    assert before == (readme.read_bytes(), readme.stat().st_mtime_ns)


def test_default_scaffold_can_safely_transition_to_reference_corpus(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    initialize_project(root, version=TEST_VERSION)
    collection_readme = root / "docs/adr/README.md"
    before = collection_readme.read_bytes()

    plan = initialize_project(root, version=TEST_VERSION, with_reference_corpus=True)

    actions = {operation.path.as_posix(): operation.action for operation in plan.operations}
    assert not plan.has_conflicts
    assert actions["tools/desys_indexer.yaml"] == "UPDATE"
    assert actions["docs/desys/README.md"] == "UPDATE"
    assert actions["AGENTS.md"] == "UPDATE"
    assert collection_readme.read_bytes() == before
    assert (root / "docs/desys/corpus-manifest.yaml").is_file()


def test_forged_predecessor_manifest_cannot_authorize_overwrite(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    initialize_project(root, version=TEST_VERSION, with_reference_corpus=True)
    bundle = load_reference_bundle()
    target = root / bundle.entries[2].target
    local_content = b"consumer-local-content\n"
    target.write_bytes(local_content)
    manifest_path = root / "docs/desys/corpus-manifest.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    forged_checksum = f"sha256:{hashlib.sha256(local_content).hexdigest()}"
    manifest["bundle_checksum"] = f"sha256:{'f' * 64}"
    entry = next(item for item in manifest["entries"] if item["target"] == bundle.entries[2].target.as_posix())
    entry["original_checksum"] = forged_checksum
    entry["installed_checksum"] = forged_checksum
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")

    plan = initialize_project(root, version=TEST_VERSION, with_reference_corpus=True)

    manifest_operation = next(
        item
        for item in plan.operations
        if item.path.as_posix() == "docs/desys/corpus-manifest.yaml"
    )
    assert plan.has_conflicts
    assert manifest_operation.action == "CONFLICT"
    assert manifest_operation.reason == "unsupported prior corpus bundle"
    assert target.read_bytes() == local_content
    assert all(
        operation.action not in {"UPDATE", "DELETE"}
        for operation in plan.operations
        if operation.path == bundle.entries[2].target
    )


def test_trusted_v02_predecessor_is_validated_without_planning_writes(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    initialize_project(root, version=TEST_VERSION, with_reference_corpus=True)
    manifest_path = write_v02_predecessor_manifest(root)
    before = {
        path: (path.read_bytes(), path.stat().st_mtime_ns)
        for path in root.rglob("*")
        if path.is_file() and ".git" not in path.parts
    }

    plan = initialize_project(root, version=TEST_VERSION)

    operation = next(item for item in plan.operations if item.path == init_project_module.CORPUS_MANIFEST_PATH)
    assert not plan.has_conflicts
    assert plan.cross_snapshot
    assert operation.action == "UPDATE"
    assert operation.reason == (
        f"commit migration from {V02_BUNDLE_CHECKSUM} to {load_reference_bundle().bundle_checksum}"
    )
    corpus_actions = {
        item.action
        for item in plan.operations
        if item.path.is_relative_to(init_project_module.REFERENCE_ROOT)
        or item.path.name in {"LICENSE", "THIRD_PARTY_NOTICES.md"}
    }
    assert corpus_actions == {"UNCHANGED"}
    assert manifest_path.is_file()
    assert {
        path: (path.read_bytes(), path.stat().st_mtime_ns)
        for path in root.rglob("*")
        if path.is_file() and ".git" not in path.parts
    } == before


def test_cross_snapshot_dry_run_and_apply_return_the_same_zero_write_plan(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    initialize_project(root, version=TEST_VERSION, with_reference_corpus=True)
    write_v02_predecessor_manifest(root)
    before = {
        path: (path.read_bytes(), path.stat().st_mtime_ns)
        for path in root.rglob("*")
        if path.is_file() and ".git" not in path.parts
    }

    dry_run = initialize_project(root, dry_run=True, version=TEST_VERSION)
    apply = initialize_project(root, version=TEST_VERSION)

    assert dry_run == apply
    assert init_project_module.render_plan(dry_run) == init_project_module.render_plan(apply)
    assert {
        path: (path.read_bytes(), path.stat().st_mtime_ns)
        for path in root.rglob("*")
        if path.is_file() and ".git" not in path.parts
    } == before


@pytest.mark.parametrize(
    ("change", "reason"),
    [
        ("modify", "managed corpus file was modified locally"),
        ("delete", "managed corpus file was deleted locally"),
    ],
)
def test_cross_snapshot_rejects_local_predecessor_changes(
    tmp_path: Path,
    change: str,
    reason: str,
) -> None:
    root = make_repository(tmp_path / "repository")
    initialize_project(root, version=TEST_VERSION, with_reference_corpus=True)
    write_v02_predecessor_manifest(root)
    target = root / load_reference_bundle().entries[0].target
    if change == "modify":
        target.write_bytes(b"consumer change\n")
    else:
        target.unlink()

    plan = initialize_project(root, version=TEST_VERSION)

    conflict = next(operation for operation in plan.operations if operation.path == target.relative_to(root))
    assert plan.has_conflicts
    assert conflict.action == "CONFLICT"
    assert conflict.reason == reason


def test_cross_snapshot_identity_conflict_names_consumer_and_target(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    initialize_project(root, version=TEST_VERSION, with_reference_corpus=True)
    write_v02_predecessor_manifest(root)
    entry = next(item for item in load_reference_bundle().entries if item.indexable)
    consumer_path = root / "docs/adr" / entry.target.name
    consumer_path.write_bytes(entry.content)

    plan = initialize_project(root, version=TEST_VERSION)

    conflicts = [
        operation
        for operation in plan.operations
        if operation.action == "CONFLICT" and "owned by consumer" in (operation.reason or "")
    ]
    assert plan.has_conflicts
    assert conflicts
    assert all(consumer_path.relative_to(root).as_posix() in (operation.reason or "") for operation in conflicts)
    assert all(operation.path == entry.target for operation in conflicts)


def test_cross_snapshot_identity_preflight_ignores_excluded_source_trees(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    initialize_project(root, version=TEST_VERSION, with_reference_corpus=True)
    write_v02_predecessor_manifest(root)
    entry = next(item for item in load_reference_bundle().entries if item.indexable)
    excluded_path = root / "docs/adr/node_modules/package" / entry.target.name
    excluded_path.parent.mkdir(parents=True)
    excluded_path.write_bytes(entry.content)

    plan = initialize_project(root, version=TEST_VERSION)

    assert not plan.has_conflicts


def test_cross_snapshot_alias_collision_preserves_consumer_authority(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    initialize_project(root, version=TEST_VERSION, with_reference_corpus=True)
    write_v02_predecessor_manifest(root)
    entry = next(item for item in load_reference_bundle().entries if item.indexable)
    metadata, body = init_project_module.parse_front_matter(entry.content.decode("utf-8"))
    metadata["document_id"] = "ADR-9999"
    metadata["canonical_id"] = "adr.consumer.local"
    metadata["aliases"] = [entry.canonical_id]
    consumer_path = root / "docs/adr/ADR-9999-consumer.md"
    consumer_path.write_text(
        f"---\n{yaml.safe_dump(metadata, sort_keys=False)}---\n{body}",
        encoding="utf-8",
    )

    plan = initialize_project(root, version=TEST_VERSION)

    conflict = next(
        operation
        for operation in plan.operations
        if operation.path == entry.target and "conflicts with alias owned by consumer" in (operation.reason or "")
    )
    assert plan.has_conflicts
    assert consumer_path.relative_to(root).as_posix() in (conflict.reason or "")


def test_cross_snapshot_rejects_portable_path_collision(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    initialize_project(root, version=TEST_VERSION, with_reference_corpus=True)
    write_v02_predecessor_manifest(root)
    target = PurePosixPath("docs/desys/LICENSE")
    collision = root / "DOCS/DESYS/LICENSE"
    collision.parent.mkdir(parents=True)
    collision.write_bytes(b"consumer path\n")

    plan = initialize_project(root, version=TEST_VERSION)

    conflict = next(
        operation
        for operation in plan.operations
        if operation.path == target and "portable path collides" in (operation.reason or "")
    )
    assert plan.has_conflicts
    assert collision.relative_to(root).as_posix() in (conflict.reason or "")
    assert any(
        operation.path == PurePosixPath("docs")
        and "existing path DOCS" in (operation.reason or "")
        for operation in plan.operations
    )


def test_future_skill_identifier_namespace_uses_shared_collision_preflight() -> None:
    consumer = init_project_module.IdentityRecord(
        "skill_id",
        "skill.example",
        PurePosixPath(".agents/skills/example/SKILL.md"),
        "consumer",
    )
    target = init_project_module.IdentityRecord(
        "skill_id",
        "skill.example",
        PurePosixPath("docs/desys/reference/skills/DSK-001-example.md"),
        "target corpus",
    )

    conflicts = init_project_module._identity_conflicts([target, consumer])

    assert len(conflicts) == 1
    assert conflicts[0].path == target.path
    assert consumer.path.as_posix() in (conflicts[0].reason or "")
    assert "owned by consumer" in (conflicts[0].reason or "")


def test_cross_snapshot_planner_emits_every_non_conflict_operation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = make_repository(tmp_path / "repository")
    reference = PurePosixPath("docs/desys/reference/test")
    old_contents = {
        reference / "same.txt": b"same\n",
        reference / "update.txt": b"old\n",
        reference / "rename-old.txt": b"rename\n",
    }
    new_contents = {
        reference / "same.txt": b"same\n",
        reference / "update.txt": b"new\n",
        reference / "rename-new.txt": b"rename\n",
    }
    for target, content in old_contents.items():
        destination = root / target
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)

    def checksum(content: bytes) -> str:
        return f"sha256:{hashlib.sha256(content).hexdigest()}"

    descriptor_entries = tuple(
        DescriptorEntry(
            source=target.name,
            target=target,
            collection="test",
            classification="navigation",
            indexable=False,
            checksum=checksum(content),
        )
        for target, content in sorted(old_contents.items(), key=lambda item: item[0].as_posix())
    )
    bundle_entries = tuple(
        BundleEntry(
            source=target.name,
            target=target,
            collection="test",
            classification="navigation",
            indexable=False,
            checksum=checksum(content),
            content=content,
        )
        for target, content in sorted(new_contents.items(), key=lambda item: item[0].as_posix())
    )
    predecessor_checksum = f"sha256:{'1' * 64}"
    target_checksum = f"sha256:{'2' * 64}"
    descriptor = PredecessorDescriptor(
        descriptor_schema="1.0.0",
        target_bundle_checksum=target_checksum,
        accepted_manifest_schemas=("1.1.0",),
        predecessor_package_version="0.2.0a1",
        bundle_schema="1.1.0",
        inventory_schema="1.0.0",
        corpus_version="0.2.0-alpha.1",
        release_tag="v0.2.0-alpha.1",
        source_commit="1" * 40,
        bundle_checksum=predecessor_checksum,
        entries=descriptor_entries,
    )
    bundle = ReferenceBundle(
        bundle_schema="1.1.0",
        inventory_schema="1.0.0",
        corpus_version="0.3.0-alpha.1",
        release_tag="v0.3.0-alpha.1",
        source_commit="2" * 40,
        bundle_checksum=target_checksum,
        entries=bundle_entries,
    )
    manifest = ConsumerManifest(
        manifest_schema="1.1.0",
        package_name="dundercode-engineering-system",
        package_version="0.2.0a1",
        package_source="dundercode-engineering-system==0.2.0a1",
        release_tag="v0.2.0-alpha.1",
        source_commit="1" * 40,
        corpus_version="0.2.0-alpha.1",
        bundle_checksum=predecessor_checksum,
        entries=(),
    )
    monkeypatch.setattr(init_project_module, "render_consumer_manifest", lambda *args, **kwargs: b"target manifest\n")

    first = init_project_module._plan_cross_snapshot_corpus(
        root,
        bundle,
        manifest,
        descriptor,
        TEST_VERSION,
        f"dundercode-engineering-system=={TEST_VERSION}",
        b"predecessor manifest\n",
    )
    second = init_project_module._plan_cross_snapshot_corpus(
        root,
        bundle,
        manifest,
        descriptor,
        TEST_VERSION,
        f"dundercode-engineering-system=={TEST_VERSION}",
        b"predecessor manifest\n",
    )

    actions = {operation.path.name: operation.action for operation in first}
    assert actions == {
        "corpus-manifest.yaml": "UPDATE",
        "rename-new.txt": "ADD",
        "rename-old.txt": "REMOVE",
        "same.txt": "UNCHANGED",
        "update.txt": "UPDATE",
    }
    assert first == second
    rename_add = next(operation for operation in first if operation.path.name == "rename-new.txt")
    rename_remove = next(operation for operation in first if operation.path.name == "rename-old.txt")
    assert rename_add.target_checksum == rename_remove.expected_checksum

    manifest_path = root / init_project_module.CORPUS_MANIFEST_PATH
    manifest_path.write_bytes(b"predecessor manifest\n")
    monkeypatch.setattr(init_project_module, "load_reference_bundle", lambda: bundle)

    def unsupported_predecessor(*args, **kwargs):
        raise init_project_module.UnsupportedCorpusBundleError("synthetic predecessor")

    monkeypatch.setattr(init_project_module, "load_consumer_manifest", unsupported_predecessor)
    monkeypatch.setattr(
        init_project_module,
        "validate_predecessor_manifest",
        lambda *args, **kwargs: (manifest, descriptor),
    )
    before = {
        path: (path.read_bytes(), path.stat().st_mtime_ns)
        for path in root.rglob("*")
        if path.is_file() and ".git" not in path.parts
    }

    dry_run = initialize_project(root, dry_run=True, version=TEST_VERSION)
    apply = initialize_project(root, version=TEST_VERSION)

    assert dry_run == apply
    assert not dry_run.has_conflicts
    assert dry_run.cross_snapshot
    integrated_actions = {
        operation.path.name: operation.action
        for operation in dry_run.operations
        if operation.path.parent == reference
    }
    assert integrated_actions == {
        "rename-new.txt": "ADD",
        "rename-old.txt": "REMOVE",
        "same.txt": "UNCHANGED",
        "update.txt": "UPDATE",
    }
    assert init_project_module.render_plan(dry_run) == init_project_module.render_plan(apply)
    assert {
        path: (path.read_bytes(), path.stat().st_mtime_ns)
        for path in root.rglob("*")
        if path.is_file() and ".git" not in path.parts
    } == before


def test_forged_declared_predecessor_manifest_is_rejected_before_ownership(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    initialize_project(root, version=TEST_VERSION, with_reference_corpus=True)
    manifest_path = write_v02_predecessor_manifest(root)
    payload = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    payload["entries"][0]["installed_checksum"] = f"sha256:{'f' * 64}"
    manifest_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    legal_file = root / "docs/desys/LICENSE"
    before = legal_file.read_bytes()

    plan = initialize_project(root, version=TEST_VERSION)

    operation = next(item for item in plan.operations if item.path == init_project_module.CORPUS_MANIFEST_PATH)
    assert plan.has_conflicts
    assert operation.reason == (
        "invalid predecessor corpus manifest: "
        "Consumer manifest entries do not match its predecessor descriptor."
    )
    assert legal_file.read_bytes() == before


def test_forged_predecessor_manifest_cannot_authorize_delete(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    initialize_project(root, version=TEST_VERSION, with_reference_corpus=True)
    victim = root / "docs/desys/reference/consumer/victim.txt"
    victim.parent.mkdir()
    victim.write_bytes(b"consumer-owned\n")
    manifest_path = root / "docs/desys/corpus-manifest.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    victim_checksum = f"sha256:{hashlib.sha256(victim.read_bytes()).hexdigest()}"
    manifest["bundle_checksum"] = f"sha256:{'e' * 64}"
    manifest["entries"].append(
        {
            "source": "consumer/victim.txt",
            "target": "docs/desys/reference/consumer/victim.txt",
            "collection": "consumer",
            "classification": "navigation",
            "distribution": "approved",
            "original_checksum": victim_checksum,
            "installed_checksum": victim_checksum,
            1: "must not be trusted for an unsupported bundle",
        }
    )
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")

    plan = initialize_project(root, version=TEST_VERSION)

    manifest_operation = next(
        item
        for item in plan.operations
        if item.path.as_posix() == "docs/desys/corpus-manifest.yaml"
    )
    assert plan.has_conflicts
    assert manifest_operation.reason == (
        "invalid corpus ownership manifest: Consumer manifest entry 41 must use string field names."
    )
    assert victim.read_bytes() == b"consumer-owned\n"
    assert all(operation.path.as_posix() != "docs/desys/reference/consumer/victim.txt" for operation in plan.operations)


def test_complete_preapply_validation_detects_post_plan_change(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    root = make_repository(tmp_path / "repository")
    initialize_project(root, version=TEST_VERSION, with_reference_corpus=True)
    bundle = load_reference_bundle()
    changed = root / bundle.entries[-1].target
    missing_scaffold = root / ".github/workflows/desys-docs-quality.yml"
    missing_scaffold.unlink()
    original_validate = init_project_module._validate_plan_safety

    def change_after_plan(repository: Path, plan: init_project_module.InitializationPlan) -> None:
        changed.write_bytes(changed.read_bytes() + b"\nlate local change\n")
        original_validate(repository, plan)

    monkeypatch.setattr(init_project_module, "_validate_plan_safety", change_after_plan)

    with pytest.raises(ProjectInitializationError, match="changed after planning"):
        initialize_project(root, version=TEST_VERSION)

    assert not missing_scaffold.exists()
    assert changed.read_bytes().endswith(b"late local change\n")


def test_preapply_validation_detects_late_unmanaged_reference_path(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = make_repository(tmp_path / "repository")
    initialize_project(root, version=TEST_VERSION, with_reference_corpus=True)
    manifest = root / "docs/desys/corpus-manifest.yaml"
    before = (manifest.read_bytes(), manifest.stat().st_mtime_ns)
    unmanaged = root / "docs/desys/reference/knowledge/consumer.md"
    original_validate = init_project_module._validate_plan_safety

    def add_after_plan(repository: Path, plan: init_project_module.InitializationPlan) -> None:
        unmanaged.write_bytes(b"consumer owned\n")
        original_validate(repository, plan)

    monkeypatch.setattr(init_project_module, "_validate_plan_safety", add_after_plan)

    with pytest.raises(ProjectInitializationError, match="Reference namespace changed after planning"):
        initialize_project(root, version=TEST_VERSION)

    assert unmanaged.read_bytes() == b"consumer owned\n"
    assert (manifest.read_bytes(), manifest.stat().st_mtime_ns) == before


def test_conflict_prevents_all_writes(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    tools = root / "tools"
    tools.mkdir()
    config = tools / "desys_indexer.yaml"
    config.write_text("consumer-owned: true\n", encoding="utf-8")

    plan = initialize_project(root, version=TEST_VERSION)

    assert plan.has_conflicts
    assert config.read_text(encoding="utf-8") == "consumer-owned: true\n"
    assert not (root / "docs").exists()
    assert not (root / ".gitignore").exists()


def test_extends_existing_gitignore_once(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    gitignore = root / ".gitignore"
    gitignore.write_text(".venv/\n", encoding="utf-8")

    first = initialize_project(root, version=TEST_VERSION)
    second = initialize_project(root, version=TEST_VERSION)
    content = gitignore.read_text(encoding="utf-8")

    assert "UPDATE" in {operation.action for operation in first.operations}
    assert not second.has_conflicts
    assert content.count("/docs/generated/") == 1
    assert content.count("Regenerated by scripts/desys-docs-quality.sh") == 1
    assert content.startswith(".venv/\n\n")


def test_extends_existing_agents_file_once(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    agents = root / "AGENTS.md"
    agents.write_text("# Existing Agent Instructions\n", encoding="utf-8")

    first = initialize_project(root, version=TEST_VERSION)
    second = initialize_project(root, version=TEST_VERSION)
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

    plan = initialize_project(root, version=TEST_VERSION)

    assert plan.has_conflicts
    assert agents.read_text(encoding="utf-8") == original
    assert not (root / "docs").exists()


def test_preserves_full_sha_git_source(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    source = (
        "dundercode-engineering-system @ "
        f"git+https://github.com/DunderCode-Solutions/dundercode-engineering-system.git@{'a' * 40}"
    )

    initialize_project(root, version=TEST_VERSION, desys_source=source)

    assert (root / "tools/desys-source.txt").read_text(encoding="utf-8") == f"{source}\n"


def test_accepts_repository_relative_wheel_source(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    vendor = root / "tools/vendor"
    vendor.mkdir(parents=True)
    wheel = vendor / "dundercode_engineering_system-0.3.0a1-py3-none-any.whl"
    wheel.write_bytes(b"pilot wheel")
    source = wheel.relative_to(root).as_posix()

    initialize_project(root, version=TEST_VERSION, desys_source=source)

    assert (root / "tools/desys-source.txt").read_text(encoding="utf-8") == f"{source}\n"


def test_rejects_mutable_or_unsafe_sources_before_writing(tmp_path: Path) -> None:
    invalid_sources = (
        "",
        " dundercode-engineering-system==0.3.0a1",
        "dundercode-engineering-system>=0.3.0a1",
        "dundercode-engineering-system==1..0",
        "dundercode-engineering-system==01.2.3",
        "dundercode-engineering-system==0.2.0",
        "dundercode-engineering-system @ git+https://example.com/desys.git@main",
        "dundercode-engineering-system @ git+http://example.com/desys.git@" + "a" * 40,
        "dundercode-engineering-system @ git+https://example.com/desys.git?token=secret@" + "a" * 40,
        "/tmp/desys.whl",
        "../desys.whl",
        "tools/desys release.whl",
        "desys\nsecond-line",
    )

    for index, source in enumerate(invalid_sources):
        root = make_repository(tmp_path / f"repository-{index}")
        with pytest.raises(ProjectInitializationError):
            initialize_project(root, version=TEST_VERSION, desys_source=source)
        assert [path.name for path in root.iterdir()] == [".git"]


def test_source_change_is_a_non_destructive_conflict(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    initialize_project(root, version=TEST_VERSION)
    source_file = root / "tools/desys-source.txt"
    original = source_file.read_bytes()
    git_source = (
        "dundercode-engineering-system @ "
        f"git+https://example.com/desys.git@{'b' * 40}"
    )

    plan = initialize_project(root, version=TEST_VERSION, desys_source=git_source)

    source_operation = next(
        operation for operation in plan.operations if operation.path.as_posix() == "tools/desys-source.txt"
    )
    assert plan.has_conflicts
    assert source_operation.action == "CONFLICT"
    assert source_file.read_bytes() == original


def fake_uvx_environment(tmp_path: Path) -> tuple[dict[str, str], Path]:
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    marker = tmp_path / "uvx-called"
    fake_uvx = fake_bin / "uvx"
    fake_uvx.write_bytes(b'#!/usr/bin/env bash\nprintf "%s\\n" "$*" >> "$UVX_MARKER"\n')
    fake_uvx.chmod(0o755)
    return (
        {
            **os.environ,
            "PATH": f"{fake_bin.as_posix()}{os.pathsep}{os.environ['PATH']}",
            "UVX_MARKER": marker.as_posix(),
        },
        marker,
    )


def bash_executable() -> str:
    candidate = shutil.which("bash")
    if candidate is None:
        raise RuntimeError("Bash is required for the generated quality-script tests.")
    return candidate


def test_quality_script_accepts_source_without_terminal_newline(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    initialize_project(root, version=TEST_VERSION)
    source_file = root / "tools/desys-source.txt"
    source_file.write_text("dundercode-engineering-system==0.3.0a1", encoding="utf-8")
    environment, marker = fake_uvx_environment(tmp_path)

    result = subprocess.run(
        [bash_executable(), (root / "scripts/desys-docs-quality.sh").as_posix()],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
        env=environment,
    )

    assert result.returncode == 0, result.stderr
    assert marker.read_text(encoding="utf-8").count("dundercode-engineering-system==0.3.0a1") == 3


def test_quality_script_rejects_tampered_source_before_uvx(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    initialize_project(root, version=TEST_VERSION)
    (root / "tools/desys-source.txt").write_text(
        "dundercode-engineering-system>=0.3.0a1\n",
        encoding="utf-8",
    )
    environment, marker = fake_uvx_environment(tmp_path)

    result = subprocess.run(
        [bash_executable(), (root / "scripts/desys-docs-quality.sh").as_posix()],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
        env=environment,
    )

    assert result.returncode == 1
    assert "Unsupported or mutable DESys source" in result.stderr
    assert not marker.exists()


def test_quality_script_rejects_multiple_source_lines_before_uvx(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    initialize_project(root, version=TEST_VERSION)
    (root / "tools/desys-source.txt").write_text(
        "dundercode-engineering-system==0.3.0a1\nsecond-source\n",
        encoding="utf-8",
    )
    environment, marker = fake_uvx_environment(tmp_path)

    result = subprocess.run(
        [bash_executable(), (root / "scripts/desys-docs-quality.sh").as_posix()],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
        env=environment,
    )

    assert result.returncode == 1
    assert "must contain exactly one non-empty line" in result.stderr
    assert not marker.exists()


def test_rejects_non_git_root(tmp_path: Path) -> None:
    with pytest.raises(ProjectInitializationError):
        initialize_project(tmp_path, dry_run=True, version=TEST_VERSION)


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

    plan = initialize_project(root, version=TEST_VERSION)

    assert plan.has_conflicts
    assert not (root / "tools").exists()
