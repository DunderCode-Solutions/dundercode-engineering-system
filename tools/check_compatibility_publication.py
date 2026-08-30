"""Validate release evidence and its canonically rendered compatibility publication."""

from __future__ import annotations

import argparse
import json
import sys
import tomllib
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.desys_metadata import UniqueKeyLoader

DEFAULT_EVIDENCE = Path("docs/release-evidence/v0.3.0a1-development-candidate.yaml")
DEFAULT_SCHEMA = Path("docs/release-evidence/release-evidence-1.0.0.schema.json")
DEFAULT_DOCUMENT = Path("docs/DESYS-V0.3-COMPATIBILITY.md")
BEGIN_MARKER = "<!-- BEGIN GENERATED COMPATIBILITY PUBLICATION -->"
END_MARKER = "<!-- END GENERATED COMPATIBILITY PUBLICATION -->"
REPOSITORY_URL = "https://github.com/DunderCode-Solutions/dundercode-engineering-system"
ROOT_SUMMARY_LINK = "[`docs/DESYS-V0.3-COMPATIBILITY.md`](docs/DESYS-V0.3-COMPATIBILITY.md)"
DOCS_SUMMARY_LINK = "[`DESYS-V0.3-COMPATIBILITY.md`](DESYS-V0.3-COMPATIBILITY.md)"
SUMMARY_LINKS = {
    Path("SUPPORTED-PLATFORMS.md"): ROOT_SUMMARY_LINK,
    Path("RELEASE_NOTES.md"): ROOT_SUMMARY_LINK,
    Path("CHANGELOG.md"): ROOT_SUMMARY_LINK,
    Path("docs/README.md"): DOCS_SUMMARY_LINK,
    Path("docs/DESYS-SKILLS-COMPATIBILITY-DELIVERY-ROADMAP.md"): DOCS_SUMMARY_LINK,
}
SUMMARY_DOCUMENTS = tuple(SUMMARY_LINKS)
SUPPORTED_CAPABILITIES = (
    "predecessor-validation",
    "deterministic-planning",
    "transactional-apply",
    "apply-failure-automatic-rollback",
    "interrupted-transaction-recovery",
)
REFUSAL_CAPABILITIES = ("transaction-refusal", "pending-state-guard")
CONTRACT_CHECKSUM_FIELDS = {
    "reference_bundle_schema": "reference_bundle_schema_checksum",
    "consumer_manifest_schema": "consumer_manifest_schema_checksum",
    "compatibility_schema": "compatibility_schema_checksum",
    "predecessor_descriptor_schema": "predecessor_descriptor_schema_checksum",
}
TRUSTED_PREDECESSORS = {
    "sha256:d78bb3a685bf285f29d542d1709be9874842f759f00d9739ba073ce94633f62a": {
        "predecessor_package_version": "0.2.0a1",
        "predecessor_release_label": "v0.2.0-alpha.1",
        "predecessor_release_commit": "d736b028b285a3c4f4d22b685ddd5a0903c9822d",
        "predecessor_release_url": (
            "https://github.com/DunderCode-Solutions/dundercode-engineering-system/tree/v0.2.0-alpha.1"
        ),
        "predecessor_corpus_source_commit": "1ba18c126dc9adf035f64c0ca6eda75186e73b60",
        "tracked_evidence": Path("docs/pilot/TAG-001-V0.2-ANONYMOUS-PUBLIC-TAG-EVIDENCE.md"),
    }
}


class PublicationError(ValueError):
    """Raised when release evidence or publication text is invalid or stale."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise PublicationError(message)


def load_yaml(path: Path) -> dict[str, Any]:
    """Load a unique-key YAML mapping."""
    try:
        payload = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    except yaml.YAMLError as error:
        raise PublicationError(f"Invalid YAML in {path}: {error}") from error
    _require(isinstance(payload, dict), f"{path} must contain a YAML mapping.")
    return payload


def validate_publication(
    evidence: dict[str, Any],
    schema: dict[str, Any],
    repository_root: Path,
) -> None:
    """Validate evidence and cross-check packaged distribution contracts."""
    Draft202012Validator.check_schema(schema)
    errors = sorted(Draft202012Validator(schema).iter_errors(evidence), key=lambda error: list(error.absolute_path))
    if errors:
        error = errors[0]
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        raise PublicationError(f"Release evidence schema violation at {location}: {error.message}")

    artifact = evidence["artifact"]
    candidate = evidence["candidate"]
    _require(candidate["candidate_commit"] == artifact["identifier"], "Candidate commit differs from artifact identifier.")
    _require(
        candidate["corpus_source_commit"] != artifact["identifier"],
        "Corpus provenance must remain separately identified from the candidate artifact.",
    )
    _require(artifact["url"] == f"{REPOSITORY_URL}/commit/{artifact['identifier']}", "Artifact URL is not bound to its commit.")

    pyproject = tomllib.loads((repository_root / "pyproject.toml").read_text(encoding="utf-8"))
    project = pyproject["project"]
    _require(candidate["package_name"] == project["name"], "Evidence package name differs from pyproject.toml.")
    _require(candidate["package_version"] == project["version"], "Evidence package version differs from pyproject.toml.")
    _require(project["requires-python"] == ">=3.12,<3.13", "Package support must remain the Python 3.12.x range.")

    package_root = repository_root / "tools/reference_corpus_data"
    compatibility = load_yaml(package_root / "compatibility.yaml")
    profiles = [profile for profile in compatibility["profiles"] if profile["package_version"] == candidate["package_version"]]
    _require(len(profiles) == 1, "Packaged compatibility must contain exactly one candidate profile.")
    profile = profiles[0]
    profile_fields = (
        ("release_label", "release_tag"),
        ("corpus_source_commit", "source_commit"),
        ("corpus_version", "corpus_version"),
        ("inventory_schema", "inventory_schema"),
        ("bundle_schema", "bundle_schema"),
        ("consumer_manifest_schema", "consumer_manifest_schema"),
        ("metadata_schema", "metadata_schema"),
        ("bundle_checksum", "bundle_checksum"),
    )
    for evidence_field, profile_field in profile_fields:
        _require(
            candidate[evidence_field] == profile[profile_field],
            f"Evidence {evidence_field} differs from packaged compatibility.",
        )
    _require(
        candidate["compatibility_schema"] == compatibility["compatibility_schema"],
        "Evidence compatibility schema differs from packaged compatibility.",
    )
    for evidence_field, profile_field in CONTRACT_CHECKSUM_FIELDS.items():
        _require(
            candidate["contract_checksums"][evidence_field] == profile[profile_field],
            f"Evidence {evidence_field} checksum differs from packaged compatibility.",
        )
    _require(set(profile["platforms"]) == {"linux", "macos"}, "Packaged transaction platforms must be Linux and macOS only.")

    hosts = evidence["hosts"]
    host_by_id = {host["id"]: host for host in hosts}
    _require(len(host_by_id) == len(hosts), "Host IDs must be unique.")
    supported = [host for host in hosts if host["support_level"] == "transaction-support"]
    refused = [host for host in hosts if host["support_level"] == "refusal-only"]
    _require(
        {host["platform"] for host in supported} == set(profile["platforms"]),
        "Evidence must cover each packaged support platform exactly once.",
    )
    _require(len(supported) == len(profile["platforms"]), "Evidence contains duplicate supported platform hosts.")
    _require(
        {host["platform"] for host in refused} == {"windows"} and len(refused) == 1,
        "Windows must have exactly one refusal-only host.",
    )
    for host in supported:
        _require(tuple(host["capabilities"]) == SUPPORTED_CAPABILITIES, f"Unsupported capability set for {host['id']}.")
    _require(
        tuple(refused[0]["capabilities"]) == REFUSAL_CAPABILITIES,
        "Windows capabilities must be refusal and pending-state guards only.",
    )
    _require(
        all(host["uv_version"] == candidate["uv_version"] for host in hosts),
        "Host uv versions must match the candidate evidence.",
    )

    run_by_id, job_by_id = _validate_runs(evidence, host_by_id)
    paths = evidence["migration_paths"]
    declared_predecessors = {item["bundle_checksum"] for item in profile["direct_predecessors"]}
    evidenced_predecessors = {path["predecessor_bundle_checksum"] for path in paths}
    _require(
        evidenced_predecessors == declared_predecessors,
        "Evidence paths must cover every and only packaged direct predecessor.",
    )
    _require(len(paths) == len(declared_predecessors), "Each direct predecessor must have exactly one evidence path.")
    for path in paths:
        _validate_trusted_predecessor(path, repository_root)
        descriptor_name = path["predecessor_bundle_checksum"].replace(":", "-") + ".yaml"
        descriptor = load_yaml(package_root / "predecessors" / descriptor_name)
        predecessor_fields = (
            ("predecessor_package_version", "predecessor_package_version"),
            ("predecessor_release_label", "release_tag"),
            ("predecessor_corpus_source_commit", "source_commit"),
            ("predecessor_bundle_checksum", "bundle_checksum"),
        )
        for evidence_field, descriptor_field in predecessor_fields:
            _require(
                path[evidence_field] == descriptor[descriptor_field],
                f"Evidence {evidence_field} differs from its predecessor descriptor.",
            )
        _require(
            path["predecessor_release_url"] == f"{REPOSITORY_URL}/tree/{path['predecessor_release_label']}",
            "Predecessor release URL is not bound to its release label.",
        )
        _require(
            candidate["predecessor_descriptor_schema"] == descriptor["predecessor_descriptor_schema"],
            "Evidence predecessor descriptor schema differs from its descriptor.",
        )
        _require(path["target_package_version"] == candidate["package_version"], "Path target package differs from the candidate.")
        _require(path["target_release_label"] == candidate["release_label"], "Path target release label differs from the candidate.")
        _require(path["target_bundle_checksum"] == candidate["bundle_checksum"], "Path target bundle differs from the candidate.")
        _require(descriptor["target_bundle_checksum"] == candidate["bundle_checksum"], "Descriptor target bundle differs from the candidate.")
        _validate_evidence_links(path["supported_evidence"], supported, host_by_id, run_by_id, job_by_id, "supported")
        _validate_evidence_links(path["refusal_evidence"], refused, host_by_id, run_by_id, job_by_id, "refusal")


def _validate_trusted_predecessor(path: dict[str, Any], repository_root: Path) -> None:
    bundle_checksum = path["predecessor_bundle_checksum"]
    trusted = TRUSTED_PREDECESSORS.get(bundle_checksum)
    _require(trusted is not None, "Predecessor bundle has no trusted repository release evidence.")
    for field in (
        "predecessor_package_version",
        "predecessor_release_label",
        "predecessor_release_commit",
        "predecessor_release_url",
        "predecessor_corpus_source_commit",
    ):
        _require(path[field] == trusted[field], f"Evidence {field} differs from trusted predecessor release evidence.")

    tracked_evidence = (repository_root / trusted["tracked_evidence"]).read_text(encoding="utf-8")
    expected_rows = (
        f"| Public tag | `{trusted['predecessor_release_label']}` |",
        f"| Tag URL | `{trusted['predecessor_release_url']}` |",
        f"| Peeled release commit | `{trusted['predecessor_release_commit']}` |",
        f"| Package version | `{trusted['predecessor_package_version']}` |",
        f"| Corpus source commit | `{trusted['predecessor_corpus_source_commit']}` |",
        f"| Bundle checksum | `{bundle_checksum}` |",
    )
    for row in expected_rows:
        _require(row in tracked_evidence, f"Trusted predecessor evidence is stale or incomplete: {row}")


def _validate_runs(
    evidence: dict[str, Any],
    host_by_id: dict[str, dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], dict[int, tuple[dict[str, Any], dict[str, Any]]]]:
    artifact_sha = evidence["artifact"]["identifier"]
    runs = evidence["evidence_runs"]
    run_by_id = {run["id"]: run for run in runs}
    _require(len(run_by_id) == len(runs), "Evidence run IDs must be unique.")
    _require(len({run["run_id"] for run in runs}) == len(runs), "GitHub run IDs must be unique.")
    _require(len({run["url"] for run in runs}) == len(runs), "Evidence run URLs must be unique.")
    job_by_id: dict[int, tuple[dict[str, Any], dict[str, Any]]] = {}
    expected_names = {
        "linux": "Python 3.12",
        "macos": "Python 3.12 / macos-latest",
        "windows": "Python 3.12 / windows-latest",
    }
    for run in runs:
        _require(run["url"] == f"{REPOSITORY_URL}/actions/runs/{run['run_id']}", f"Evidence run {run['id']} URL does not match its run ID.")
        _require(run["head_sha"] == artifact_sha, f"Evidence run {run['id']} is not commit-bound to the artifact.")
        for job in run["jobs"]:
            _require(job["job_id"] not in job_by_id, "GitHub job IDs must be unique.")
            _require(
                job["url"] == f"{run['url']}/job/{job['job_id']}",
                f"Evidence job {job['job_id']} URL does not match its run and job IDs.",
            )
            host = host_by_id.get(job["host_id"])
            _require(host is not None, f"Evidence job {job['job_id']} names an unknown host.")
            _require(job["name"] == expected_names[host["platform"]], f"Evidence job {job['job_id']} has the wrong host job name.")
            _require(job["capabilities"] == host["capabilities"], f"Evidence job {job['job_id']} capabilities differ from its host.")
            job_by_id[job["job_id"]] = (run, job)
    job_host_ids = [job["host_id"] for _, job in job_by_id.values()]
    _require(
        len(job_host_ids) == len(set(job_host_ids)) and set(job_host_ids) == set(host_by_id),
        "Every host must be attributed to exactly one job with a recorded success conclusion.",
    )
    return run_by_id, job_by_id


def _validate_evidence_links(
    links: list[dict[str, Any]],
    required_hosts: list[dict[str, Any]],
    host_by_id: dict[str, dict[str, Any]],
    run_by_id: dict[str, dict[str, Any]],
    job_by_id: dict[int, tuple[dict[str, Any], dict[str, Any]]],
    label: str,
) -> None:
    linked_hosts = [link["host_id"] for link in links]
    _require(
        set(linked_hosts) == {host["id"] for host in required_hosts},
        f"Path {label} evidence does not cover all required hosts.",
    )
    _require(len(linked_hosts) == len(set(linked_hosts)), f"Path {label} evidence repeats a host.")
    for link in links:
        _require(link["host_id"] in host_by_id, f"Path {label} evidence names an unknown host.")
        run = run_by_id.get(link["evidence_run_id"])
        _require(run is not None, f"Path {label} evidence names an unknown run.")
        job_pair = job_by_id.get(link["evidence_job_id"])
        _require(job_pair is not None, f"Path {label} evidence names an unknown job.")
        job_run, job = job_pair
        _require(job_run is run, f"Path {label} evidence job does not belong to its run.")
        _require(job["host_id"] == link["host_id"], f"Path {label} evidence job does not cover its host.")


def _evidence_link_for_host(path: dict[str, Any], host_id: str) -> dict[str, Any]:
    links = (*path["supported_evidence"], *path["refusal_evidence"])
    matches = [link for link in links if link["host_id"] == host_id]
    _require(len(matches) == 1, f"Migration path must contain one evidence link for {host_id}.")
    return matches[0]


def render_publication(evidence: dict[str, Any]) -> str:
    """Render all contract-bearing compatibility publication content."""
    candidate = evidence["candidate"]
    artifact = evidence["artifact"]
    remote_verification = evidence["remote_evidence_verification"]
    run_by_id = {run["id"]: run for run in evidence["evidence_runs"]}
    job_by_id = {job["job_id"]: job for run in evidence["evidence_runs"] for job in run["jobs"]}
    lines = [
        BEGIN_MARKER,
        "# DESys v0.3 Development-Candidate Compatibility",
        "",
        "Status: DEVELOPMENT CANDIDATE, NOT A RELEASE",
        "",
        "This publication records observed compatibility for the immutable migration implementation commit",
        f"[`{artifact['identifier']}`]({artifact['url']}). It is a development candidate, not a release,",
        "and does not change the packaged compatibility profile.",
        "",
        "## Artifact Identity",
        "",
        f"- Candidate/tooling artifact: [`{artifact['identifier']}`]({artifact['url']}) (`{artifact['kind']}`).",
        f"- Corpus source commit: `{candidate['corpus_source_commit']}`. This is separately labeled corpus provenance, not the candidate artifact.",
        f"- Target package and release label: `{candidate['package_version']}` / `{candidate['release_label']}`.",
        f"- Target corpus: version `{candidate['corpus_version']}`, bundle `{candidate['bundle_checksum']}`.",
        f"- Package Python support remains `{candidate['python_support']}`; exact observed patches appear per host.",
        "",
        "## Distribution Contracts",
        "",
        "| Contract | Version | Packaged checksum |",
        "| --- | --- | --- |",
        f"| Inventory schema | `{candidate['inventory_schema']}` | identity only |",
        f"| Reference bundle schema | `{candidate['bundle_schema']}` | `{candidate['contract_checksums']['reference_bundle_schema']}` |",
        f"| Consumer manifest schema | `{candidate['consumer_manifest_schema']}` | `{candidate['contract_checksums']['consumer_manifest_schema']}` |",
        f"| Metadata schema | `{candidate['metadata_schema']}` | identity only |",
        f"| Compatibility schema | `{candidate['compatibility_schema']}` | `{candidate['contract_checksums']['compatibility_schema']}` |",
        f"| Predecessor descriptor schema | `{candidate['predecessor_descriptor_schema']}` | `{candidate['contract_checksums']['predecessor_descriptor_schema']}` |",
        "",
        "The evidence checker cross-checks these identities and available contract checksums against",
        "the packaged compatibility profile and predecessor descriptors. Inventory and metadata",
        "schema checksums are not fields in the packaged compatibility profile and are not claimed here.",
        "",
        "## Compatibility Matrix",
        "",
        "| Migration path | Host environment | Python / uv | Capability | Manually verified recorded job |",
        "| --- | --- | --- | --- | --- |",
    ]
    for path in evidence["migration_paths"]:
        for host in evidence["hosts"]:
            link = _evidence_link_for_host(path, host["id"])
            run = run_by_id[link["evidence_run_id"]]
            job = job_by_id[link["evidence_job_id"]]
            migration = (
                f"[`{path['predecessor_release_label']}`]({path['predecessor_release_url']}) "
                f"`{path['predecessor_package_version']}` `{path['predecessor_bundle_checksum']}`<br>to "
                f"`{path['target_release_label']}` `{path['target_package_version']}` `{path['target_bundle_checksum']}`"
            )
            environment = (
                f"{host['operating_system']}<br>`{host['runner_image']}` image `{host['runner_image_version']}`<br>"
                f"`{host['architecture']}`"
            )
            tools = f"{host['python_implementation']} `{host['python_version']}` / uv `{host['uv_version']}`"
            capabilities = f"**{host['support_level']}**<br>" + ", ".join(f"`{item}`" for item in host["capabilities"])
            job_evidence = (
                f"[`{job['name']}` job {job['job_id']}]({job['url']}) recorded `success`<br>"
                f"[run {run['run_id']}]({run['url']}) recorded `push` / `success`<br>recorded head `{run['head_sha']}`"
            )
            lines.append(f"| {migration} | {environment} | {tools} | {capabilities} | {job_evidence} |")

    lines.extend(["", "## Predecessor Provenance", ""])
    for path in evidence["migration_paths"]:
        lines.extend(
            [
                f"- Published package tag: [`{path['predecessor_release_label']}`]({path['predecessor_release_url']}).",
                f"- Peeled package release commit: `{path['predecessor_release_commit']}`.",
                f"- Predecessor corpus source commit: `{path['predecessor_corpus_source_commit']}`.",
                f"- Predecessor bundle: `{path['predecessor_bundle_checksum']}`.",
            ]
        )
    lines.extend(
        [
            "",
            "## Evidence Boundary",
            "",
            f"The GitHub run and job metadata recorded above was manually verified on `{remote_verification['verified_on']}`",
            f"using method `{remote_verification['method']}` and is retained as evidence about migration implementation commit",
            f"`{artifact['identifier']}`. The recorded conclusions are not cryptographically authenticated by this checker.",
            "",
            remote_verification["checker_limitation"],
            "The linked implementation runs do not contain this PR's release-evidence schema, canonical publication renderer,",
            "or stale-document tests. This uncommitted working tree can only exercise those controls locally. PR5 completion",
            "may be recorded only after this diff is committed, passes CI, and merges. Final immutable tag and wheel evidence",
            "also remain pending release gates and require an evidence-record update before release.",
            "",
            "Every packaged direct predecessor has path evidence on both supported transaction hosts and separate",
            "Windows refusal evidence. Windows is not a transaction-support host: apply and recovery refuse before",
            "mutation, while pending-state guards continue to block DESys operations.",
            "",
            "## Skill Scope",
            "",
            f"- Reference Skills: {evidence['skills']['reference_skills']}.",
            f"- Active Skills: {evidence['skills']['active_skills'].replace('-', ' ')}.",
            "",
            "This candidate publishes corpus migration compatibility only. It does not approve, install, activate,",
            "or execute Skills.",
            "",
            "## Upgrade Procedure",
            "",
            "1. Start from one exact predecessor listed in the matrix and retain its manifest unchanged.",
            "2. Create and verify a repository backup that restores the complete worktree, Git metadata, managed corpus bytes, and manifest.",
            "3. Use one of the exact supported host commands below. Each command verifies uv before invoking the candidate.",
            "4. Review every `ADD`, `UPDATE`, `REMOVE`, `UNCHANGED`, or `CONFLICT`; do not apply a conflicting plan.",
            "5. Remove `--dry-run` only after review, then run consumer quality checks and verify the target manifest.",
            "",
        ]
    )
    for host in (item for item in evidence["hosts"] if item["support_level"] == "transaction-support"):
        lines.extend(_render_host_command(host, artifact, recovery=False))
    lines.extend(
        [
            "## Refusal Procedure",
            "",
            "1. Preserve unknown, skipped, altered, or forged predecessor state and its diagnostic; never edit a manifest to bypass validation.",
            "2. On Windows, cross-snapshot apply must refuse before mutation. This is the supported Windows result, not transaction support.",
            "3. If pending state exists on Windows, stop DESys operations and move the unchanged worktree and state to a supported host for recovery.",
            "",
            "## Recovery Procedure",
            "",
            "1. Stop repository writers and preserve all transaction directories, intermediates, managed files, and the verified backup.",
            "2. On a supported host, use the matching exact command below. Recovery uses the same SHA-pinned candidate as apply.",
            "3. Verify exact predecessor bytes after `restored`, or exact target bytes after authenticated committed cleanup.",
            "4. Preserve the repository for investigation if authentication or recovery fails; never manually delete pending state.",
            "",
        ]
    )
    for host in (item for item in evidence["hosts"] if item["support_level"] == "transaction-support"):
        lines.extend(_render_host_command(host, artifact, recovery=True))
    lines.extend(
        [
            "## Rollback And Reversal",
            "",
            "Automatic rollback occurs only when transactional apply fails before a successful commit; it restores and",
            "verifies the exact predecessor. There is no `--rollback` operation. After successful apply, reversal requires",
            "restoring the complete independently verified pre-upgrade repository backup and then verifying predecessor",
            "manifest and managed checksums. Running the old package over the new manifest is unsupported.",
            "",
            "## Release Gate",
            "",
            f"- Final immutable tag evidence: {evidence['release_gate']['final_tag_evidence']}.",
            f"- Final wheel evidence: {evidence['release_gate']['wheel_evidence']}.",
            f"- Required update: {evidence['release_gate']['required_update']}",
            END_MARKER,
        ]
    )
    return "\n".join(lines)


def _render_host_command(host: dict[str, Any], artifact: dict[str, Any], *, recovery: bool) -> list[str]:
    label = "Recovery" if recovery else "Upgrade dry run"
    source = f"dundercode-engineering-system @ git+{REPOSITORY_URL}.git@{artifact['identifier']}"
    lines = [
        f"### {label}: {host['operating_system']}",
        "",
        "```bash",
        "set -euo pipefail",
        'REPOSITORY_ROOT="/absolute/path/to/consumer-repository"',
        f'UV_VERSION="{host["uv_version"]}"',
        f'DESYS_PYTHON="{host["python_version"]}"',
        f'DESYS_SOURCE="{source}"',
        'uvx --version | grep -Eq "^uvx ${UV_VERSION}( |$)"',
    ]
    if recovery:
        lines.extend(
            [
                'uvx --isolated --no-config --python "$DESYS_PYTHON" --from "$DESYS_SOURCE" \\',
                '  desys-project-init --root "$REPOSITORY_ROOT" --recover',
            ]
        )
    else:
        lines.extend(
            [
                'uvx --isolated --no-config --python "$DESYS_PYTHON" --from "$DESYS_SOURCE" \\',
                '  desys-project-init --root "$REPOSITORY_ROOT" --desys-source "$DESYS_SOURCE" \\',
                "  --with-reference-corpus --dry-run",
                "",
                "# Run only after reviewing the conflict-free dry run and verified backup.",
                'uvx --isolated --no-config --python "$DESYS_PYTHON" --from "$DESYS_SOURCE" \\',
                '  desys-project-init --root "$REPOSITORY_ROOT" --desys-source "$DESYS_SOURCE" \\',
                "  --with-reference-corpus",
            ]
        )
    lines.extend(["```", ""])
    return lines


def replace_publication(document: str, publication: str) -> str:
    """Replace exactly one marked publication block."""
    _require(document.count(BEGIN_MARKER) == 1, "Compatibility document must contain one publication start marker.")
    _require(document.count(END_MARKER) == 1, "Compatibility document must contain one publication end marker.")
    before, remainder = document.split(BEGIN_MARKER, 1)
    _, after = remainder.split(END_MARKER, 1)
    return before + publication + after


def check_publication_document(document: str, evidence: dict[str, Any]) -> None:
    """Fail when any contract-bearing publication content is stale."""
    expected = replace_publication(document, render_publication(evidence))
    _require(document == expected, "Compatibility publication is stale; run the checker with --write.")


def check_summary_documents(evidence: dict[str, Any], documents: dict[Path, str]) -> None:
    """Require canonical links and reject duplicated candidate evidence facts."""
    candidate = evidence["candidate"]
    forbidden = {
        evidence["artifact"]["identifier"],
        candidate["bundle_checksum"],
        *(host["operating_system"] for host in evidence["hosts"]),
        *(run["url"] for run in evidence["evidence_runs"]),
    }
    for path, expected_link in SUMMARY_LINKS.items():
        text = documents.get(path)
        _require(text is not None, f"Missing summary document for validation: {path}")
        _require(text.count(expected_link) == 1, f"{path} must contain exactly one canonical compatibility link.")
        duplicated = sorted(value for value in forbidden if value in text)
        _require(not duplicated, f"{path} duplicates canonical candidate evidence: {duplicated}")

    changelog = documents[Path("CHANGELOG.md")]
    _require(
        f"`{candidate['release_label']}` development" in changelog,
        "CHANGELOG.md candidate release label is stale.",
    )
    _require(
        f"direct `{evidence['migration_paths'][0]['predecessor_release_label']}` predecessor" in changelog,
        "CHANGELOG.md predecessor release label is stale.",
    )
    _require(
        "transactional\n  apply, apply-failure rollback, and authenticated interrupted-state recovery" in changelog,
        "CHANGELOG.md migration capability summary is stale.",
    )
    _require(
        "Windows cross-snapshot apply and recovery fail closed before mutation" in changelog,
        "CHANGELOG.md Windows capability summary is stale.",
    )

    checkpoint = documents[Path("docs/README.md")]
    predecessor = evidence["migration_paths"][0]
    _require(
        f"current development target is `{candidate['package_version']}` /\n`{candidate['release_label']}`" in checkpoint,
        "docs/README.md candidate version summary is stale.",
    )
    _require(
        f"published prerelease remains PEP 440 package version `{predecessor['predecessor_package_version']}` and public\n"
        f"release label `{predecessor['predecessor_release_label']}`" in checkpoint,
        "docs/README.md published predecessor version summary is stale.",
    )
    _require(
        f"`{predecessor['predecessor_release_commit']}`" in checkpoint,
        "docs/README.md predecessor release commit summary is stale.",
    )
    _require("PR5 is in progress pending committed CI and merge" in checkpoint, "docs/README.md PR5 status is stale.")
    _require(
        f"Active Skills remain {evidence['skills']['active_skills'].replace('-', ' ')}" in checkpoint,
        "docs/README.md Active Skills status is stale.",
    )

    roadmap = documents[Path("docs/DESYS-SKILLS-COMPATIBILITY-DELIVERY-ROADMAP.md")]
    pr3 = roadmap.split("### PR 3", 1)[1].split("### PR 4", 1)[0]
    pr4 = roadmap.split("### PR 4", 1)[1].split("### PR 5", 1)[0]
    pr5 = roadmap.split("### PR 5", 1)[1].split("### PR 6", 1)[0]
    _require("Status: COMPLETE" in pr3, "Roadmap PR3 status must remain COMPLETE.")
    _require("Status: COMPLETE" in pr4, "Roadmap PR4 status must remain COMPLETE.")
    _require("Status: IN PROGRESS - PENDING CI" in pr5, "Roadmap PR5 status must remain pending CI.")
    _require("Status: COMPLETE" not in pr5, "Roadmap PR5 cannot claim completion before committed CI and merge.")
    _require("passes CI, and merges" in pr5, "Roadmap PR5 completion condition is missing.")
    roadmap_predecessor_claims = (
        f"`{predecessor['predecessor_release_label']}`. Work is governed by",
        f"| Package | `{predecessor['predecessor_package_version']}` / `{predecessor['predecessor_release_label']}` |",
        f"current `{predecessor['predecessor_release_label']}` manifests validate without semantic relaxation",
        f"pin DESys to `{predecessor['predecessor_release_label']}` rather than a mutable branch",
        f"compatibility matrix names `{predecessor['predecessor_release_label']}` as a tested predecessor",
    )
    for claim in roadmap_predecessor_claims:
        _require(claim in roadmap, f"Roadmap predecessor version claim is stale: {claim}")


def parse_arguments(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, default=DEFAULT_EVIDENCE)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--document", type=Path, default=DEFAULT_DOCUMENT)
    parser.add_argument("--write", action="store_true", help="Rewrite the canonical publication after validation.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    arguments = parse_arguments(argv)
    try:
        evidence = load_yaml(arguments.evidence)
        schema = json.loads(arguments.schema.read_text(encoding="utf-8"))
        repository_root = Path(__file__).resolve().parent.parent
        validate_publication(evidence, schema, repository_root)
        document = arguments.document.read_text(encoding="utf-8")
        if arguments.write:
            arguments.document.write_text(
                replace_publication(document, render_publication(evidence)),
                encoding="utf-8",
            )
        else:
            check_publication_document(document, evidence)
        check_summary_documents(
            evidence,
            {path: (repository_root / path).read_text(encoding="utf-8") for path in SUMMARY_DOCUMENTS},
        )
    except (OSError, json.JSONDecodeError, PublicationError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Validated offline structure and internal bindings for candidate: {evidence['artifact']['identifier']}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
