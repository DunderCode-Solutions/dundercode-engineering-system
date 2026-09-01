from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from tools.check_compatibility_publication import (
    DEFAULT_DOCUMENT,
    DEFAULT_EVIDENCE,
    DEFAULT_SCHEMA,
    SUMMARY_DOCUMENTS,
    PublicationError,
    check_publication_document,
    check_summary_documents,
    load_yaml,
    render_publication,
    validate_publication,
)


@pytest.fixture
def publication() -> tuple[dict, dict]:
    return load_yaml(DEFAULT_EVIDENCE), json.loads(DEFAULT_SCHEMA.read_text(encoding="utf-8"))


def test_release_evidence_schema_and_tracked_publication_are_current(publication: tuple[dict, dict]) -> None:
    evidence, schema = publication
    Draft202012Validator.check_schema(schema)

    validate_publication(evidence, schema, Path.cwd())
    check_publication_document(DEFAULT_DOCUMENT.read_text(encoding="utf-8"), evidence)
    check_summary_documents(
        evidence,
        {path: path.read_text(encoding="utf-8") for path in SUMMARY_DOCUMENTS},
    )


@pytest.mark.parametrize(
    ("mutate", "message"),
    (
        (lambda value: value["artifact"].update(identifier="33fee4a"), "schema violation"),
        (lambda value: value["candidate"].update(bundle_schema="1.2.0"), "differs from packaged"),
        (
            lambda value: value["candidate"]["contract_checksums"].update(compatibility_schema=f"sha256:{'f' * 64}"),
            "checksum differs",
        ),
        (lambda value: value["evidence_runs"][0].update(url="https://example.com/run/1"), "schema violation"),
        (lambda value: value["evidence_runs"][0].update(head_sha="f" * 40), "not commit-bound"),
        (lambda value: value["evidence_runs"][0]["jobs"][0].update(name="Python"), "wrong host job name"),
        (
            lambda value: value["evidence_runs"][0]["jobs"][0].update(
                url="https://github.com/DunderCode-Solutions/dundercode-engineering-system/actions/runs/33280030965/job/1"
            ),
            "URL does not match",
        ),
        (lambda value: value["hosts"][0].update(python_version="3.13.0"), "schema violation"),
        (
            lambda value: value["hosts"][2]["capabilities"].append("transactional-apply"),
            "schema violation",
        ),
        (
            lambda value: value["migration_paths"][0].update(predecessor_corpus_source_commit="f" * 40),
            "differs from trusted predecessor release evidence",
        ),
        (
            lambda value: value["migration_paths"][0].update(predecessor_release_commit="f" * 40),
            "differs from trusted predecessor release evidence",
        ),
    ),
)
def test_release_evidence_rejects_invalid_contract_identity_job_and_capability(
    publication: tuple[dict, dict],
    mutate,
    message: str,
) -> None:
    evidence, schema = publication
    changed = copy.deepcopy(evidence)
    mutate(changed)

    with pytest.raises(PublicationError, match=message):
        validate_publication(changed, schema, Path.cwd())


@pytest.mark.parametrize(
    ("old", "new"),
    (
        ("Status: DEVELOPMENT CANDIDATE, NOT A RELEASE", "Status: RELEASED"),
        ("manually verified on `2026-08-29`", "automatically verified"),
        ("Corpus source commit", "Corpus revision"),
        ("Reference bundle schema", "Bundle contract"),
        ("Python 3.12 / macos-latest", "Python 3.12 / macos-26"),
        ("Final immutable tag evidence: pending", "Final immutable tag evidence: complete"),
        ('UV_VERSION="0.12.3"', 'UV_VERSION="0.12.4"'),
        ("# Run only after reviewing the conflict-free dry run", "# Apply immediately"),
    ),
)
def test_stale_publication_mutations_fail(publication: tuple[dict, dict], old: str, new: str) -> None:
    evidence, _ = publication
    current = render_publication(evidence)
    assert old in current
    stale = current.replace(old, new, 1)

    with pytest.raises(PublicationError, match="stale"):
        check_publication_document(stale, evidence)


def test_summary_link_mutation_fails(publication: tuple[dict, dict]) -> None:
    evidence, _ = publication
    documents = {path: path.read_text(encoding="utf-8") for path in SUMMARY_DOCUMENTS}
    documents[Path("RELEASE_NOTES.md")] = documents[Path("RELEASE_NOTES.md")].replace(
        "docs/DESYS-V0.3-COMPATIBILITY.md",
        "docs/STALE.md",
    )

    with pytest.raises(PublicationError, match="canonical compatibility link"):
        check_summary_documents(evidence, documents)


@pytest.mark.parametrize(
    ("path", "old", "new", "message"),
    (
        (Path("CHANGELOG.md"), "transactional\n  apply", "atomicity-free\n  apply", "capability summary"),
        (Path("docs/README.md"), "`0.3.0a1`", "`0.3.0a2`", "candidate version summary"),
        (
            Path("docs/DESYS-SKILLS-COMPATIBILITY-DELIVERY-ROADMAP.md"),
            "### PR 5 - Compatibility Publication\n\nStatus: COMPLETE",
            "### PR 5 - Compatibility Publication\n\nStatus: IN PROGRESS - PENDING CI",
            "completed publication gates",
        ),
    ),
)
def test_retained_summary_claim_mutation_fails(
    publication: tuple[dict, dict],
    path: Path,
    old: str,
    new: str,
    message: str,
) -> None:
    evidence, _ = publication
    documents = {item: item.read_text(encoding="utf-8") for item in SUMMARY_DOCUMENTS}
    documents[path] = documents[path].replace(old, new, 1)

    with pytest.raises(PublicationError, match=message):
        check_summary_documents(evidence, documents)


def test_rendered_shell_procedures_are_fail_closed_and_concrete(publication: tuple[dict, dict]) -> None:
    evidence, _ = publication
    rendered = render_publication(evidence)

    assert rendered.count("set -euo pipefail") == 4
    assert rendered.count('REPOSITORY_ROOT="/absolute/path/to/consumer-repository"') == 4
    assert rendered.count('--root "$REPOSITORY_ROOT"') == 6
    assert rendered.count('UV_VERSION="0.12.3"') == 4
    assert "<repository>" not in rendered
    assert f".git@{evidence['artifact']['identifier']}" in rendered


def test_renderer_emits_cartesian_path_host_rows(publication: tuple[dict, dict]) -> None:
    evidence, _ = publication
    expanded = copy.deepcopy(evidence)
    second = copy.deepcopy(expanded["migration_paths"][0])
    second.update(
        predecessor_package_version="0.1.0a1",
        predecessor_release_label="v0.1.0-alpha.1",
        predecessor_release_url=(
            "https://github.com/DunderCode-Solutions/dundercode-engineering-system/tree/v0.1.0-alpha.1"
        ),
        predecessor_bundle_checksum=f"sha256:{'e' * 64}",
    )
    expanded["migration_paths"].append(second)

    rendered = render_publication(expanded)

    assert rendered.count("`push` / `success`") == len(expanded["migration_paths"]) * len(expanded["hosts"])
    assert rendered.count(second["predecessor_bundle_checksum"]) == len(expanded["hosts"]) + 1
