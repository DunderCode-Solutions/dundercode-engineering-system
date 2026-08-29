from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
from copy import deepcopy
from pathlib import Path, PurePosixPath
from types import SimpleNamespace

import pytest

from tools import project_transaction as transaction_module
from tools.init_project import PlannedOperation, ProjectInitializationError, initialize_project
from tools.project_transaction import (
    STATE_DIRECTORY,
    TransactionError,
    guard_operation,
    require_no_pending_transaction,
)

MANIFEST = PurePosixPath("docs/desys/corpus-manifest.yaml")
pytestmark = pytest.mark.skipif(os.name != "posix", reason="transaction mutation protocol requires POSIX")


def authenticate_fixture(predecessor: bytes, target: bytes, entries: list[dict]) -> list[dict]:
    manifest = entries[-1]
    assert checksum(predecessor) == manifest["before_checksum"]
    assert checksum(target) == manifest["after_checksum"]
    return [
        {
            "path": entry["path"],
            "before_checksum": entry["before_checksum"],
            "after_checksum": entry["after_checksum"],
        }
        for entry in sorted(entries, key=lambda item: item["path"])
    ]


def apply_transaction(root: Path, operations: list[PlannedOperation], **kwargs) -> None:
    transaction_module.apply_transaction(
        root,
        operations,
        authenticate_record=authenticate_fixture,
        **kwargs,
    )


def recover_transaction(root: Path, **kwargs) -> str:
    kwargs.pop("validate_predecessor", None)
    return transaction_module.recover_transaction(
        root,
        authenticate_record=authenticate_fixture,
        **kwargs,
    )


def checksum(content: bytes) -> str:
    return f"sha256:{hashlib.sha256(content).hexdigest()}"


def make_repository(directory: Path) -> Path:
    directory.mkdir()
    subprocess.run(["git", "init", "--quiet", str(directory)], check=True, capture_output=True)
    return directory


def transaction_fixture(root: Path) -> tuple[list[PlannedOperation], dict[PurePosixPath, bytes]]:
    predecessor = {
        PurePosixPath("docs/desys/reference/test/update.txt"): b"old update\n",
        PurePosixPath("docs/desys/reference/test/remove.txt"): b"old remove\n",
        MANIFEST: b"predecessor manifest\n",
    }
    for relative, content in predecessor.items():
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)
    operations = [
        PlannedOperation(
            "ADD",
            PurePosixPath("docs/desys/reference/test/add.txt"),
            content=b"added\n",
            target_checksum=checksum(b"added\n"),
        ),
        PlannedOperation(
            "REMOVE",
            PurePosixPath("docs/desys/reference/test/remove.txt"),
            expected_checksum=checksum(b"old remove\n"),
        ),
        PlannedOperation(
            "UPDATE",
            PurePosixPath("docs/desys/reference/test/update.txt"),
            content=b"new update\n",
            expected_checksum=checksum(b"old update\n"),
            target_checksum=checksum(b"new update\n"),
        ),
        PlannedOperation(
            "UPDATE",
            MANIFEST,
            content=b"target manifest\n",
            expected_checksum=checksum(b"predecessor manifest\n"),
            target_checksum=checksum(b"target manifest\n"),
        ),
    ]
    return operations, predecessor


def assert_predecessor(root: Path, predecessor: dict[PurePosixPath, bytes]) -> None:
    for relative, content in predecessor.items():
        assert (root / relative).read_bytes() == content
    assert not (root / "docs/desys/reference/test/add.txt").exists()


def test_transaction_applies_add_update_remove_and_manifest_last(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    operations, _ = transaction_fixture(root)
    boundaries: list[tuple[str, PurePosixPath]] = []

    apply_transaction(
        root,
        operations,
        manifest_path=MANIFEST,
        failure_injector=lambda boundary, path: boundaries.append((boundary, path)),
    )

    assert (root / "docs/desys/reference/test/add.txt").read_bytes() == b"added\n"
    assert (root / "docs/desys/reference/test/update.txt").read_bytes() == b"new update\n"
    assert not (root / "docs/desys/reference/test/remove.txt").exists()
    assert (root / MANIFEST).read_bytes() == b"target manifest\n"
    assert [path for boundary, path in boundaries if boundary == "after_apply"][-1] == MANIFEST
    assert not (root / STATE_DIRECTORY).exists()


def test_rollback_removes_directories_created_for_added_targets(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    manifest = root / MANIFEST
    manifest.parent.mkdir(parents=True)
    manifest.write_bytes(b"predecessor manifest\n")
    added = PurePosixPath("docs/desys/reference/new/deep/added.txt")
    operations = [
        PlannedOperation("ADD", added, content=b"added\n", target_checksum=checksum(b"added\n")),
        PlannedOperation(
            "UPDATE",
            MANIFEST,
            content=b"target manifest\n",
            expected_checksum=checksum(b"predecessor manifest\n"),
            target_checksum=checksum(b"target manifest\n"),
        ),
    ]

    def inject(boundary: str, path: PurePosixPath) -> None:
        if boundary == "after_apply" and path == added:
            raise RuntimeError("injected failure after nested addition")

    with pytest.raises(TransactionError, match="exact predecessor was restored"):
        apply_transaction(root, operations, manifest_path=MANIFEST, failure_injector=inject)

    assert manifest.read_bytes() == b"predecessor manifest\n"
    assert not (root / "docs/desys/reference").exists()


@pytest.mark.parametrize("boundary", ["before_stage", "after_stage", "before_apply", "after_apply"])
@pytest.mark.parametrize("failure_index", range(4))
def test_every_injected_boundary_restores_exact_predecessor(
    tmp_path: Path,
    boundary: str,
    failure_index: int,
) -> None:
    root = make_repository(tmp_path / f"repository-{boundary}-{failure_index}")
    operations, predecessor = transaction_fixture(root)
    seen = 0

    def inject(current: str, path: PurePosixPath) -> None:
        nonlocal seen
        if current == boundary:
            if seen == failure_index:
                raise RuntimeError(f"injected {current} {path}")
            seen += 1

    with pytest.raises(TransactionError, match="exact predecessor was restored"):
        apply_transaction(root, operations, manifest_path=MANIFEST, failure_injector=inject)

    assert_predecessor(root, predecessor)
    assert not (root / STATE_DIRECTORY).exists()


def test_interrupted_rollback_blocks_operations_until_explicit_recovery(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    operations, predecessor = transaction_fixture(root)

    def interrupt(boundary: str, path: PurePosixPath) -> None:
        if boundary == "after_apply" and path.name == "add.txt":
            raise RuntimeError("injected apply failure")
        if boundary == "before_rollback" and path == MANIFEST:
            raise RuntimeError("injected rollback interruption")

    with pytest.raises(TransactionError, match="explicit recovery is required"):
        apply_transaction(root, operations, manifest_path=MANIFEST, failure_injector=interrupt)

    assert (root / STATE_DIRECTORY).is_dir()
    with pytest.raises(TransactionError, match="Pending DESys recovery"):
        require_no_pending_transaction(root)
    with pytest.raises(ProjectInitializationError, match="Pending DESys recovery"):
        initialize_project(root, dry_run=True, version="0.3.0a1")

    recover_transaction(
        root,
        manifest_path=MANIFEST,
        validate_predecessor=lambda content, entries: pytest.fail("wrong manifest")
        if content != predecessor[MANIFEST]
        else None,
    )

    assert_predecessor(root, predecessor)
    assert not (root / STATE_DIRECTORY).exists()


@pytest.mark.parametrize("boundary", ["before_rollback", "after_rollback"])
@pytest.mark.parametrize("failure_index", range(4))
def test_recovery_reruns_after_every_interrupted_rollback_boundary(
    tmp_path: Path,
    boundary: str,
    failure_index: int,
) -> None:
    root = make_repository(tmp_path / f"repository-{boundary}-{failure_index}")
    operations, predecessor = transaction_fixture(root)
    seen = 0

    def interrupt(current: str, path: PurePosixPath) -> None:
        nonlocal seen
        if current == "after_apply" and path == MANIFEST:
            raise RuntimeError("apply failure after final mutation")
        if current == boundary:
            if seen == failure_index:
                raise RuntimeError(f"rollback interruption at {path}")
            seen += 1

    with pytest.raises(TransactionError, match="explicit recovery is required"):
        apply_transaction(root, operations, manifest_path=MANIFEST, failure_injector=interrupt)

    recover_transaction(
        root,
        manifest_path=MANIFEST,
        validate_predecessor=lambda content, entries: None,
    )
    assert_predecessor(root, predecessor)


def test_forged_record_is_rejected_and_retained(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    operations, _ = transaction_fixture(root)

    def interrupt(boundary: str, path: PurePosixPath) -> None:
        if boundary == "after_apply" and path.name == "add.txt":
            raise RuntimeError("apply")
        if boundary == "before_rollback" and path == MANIFEST:
            raise RuntimeError("rollback")

    with pytest.raises(TransactionError):
        apply_transaction(root, operations, manifest_path=MANIFEST, failure_injector=interrupt)
    record_path = root / STATE_DIRECTORY / "transaction.json"
    record = json.loads(record_path.read_text(encoding="utf-8"))
    record["entries"][0]["path"] = "../../outside"
    record_path.write_text(json.dumps(record), encoding="utf-8")

    with pytest.raises(TransactionError, match="Unsafe transaction path"):
        recover_transaction(root, manifest_path=MANIFEST, validate_predecessor=lambda content, entries: None)
    assert (root / STATE_DIRECTORY).exists()


def test_symlinked_or_malformed_state_fails_closed(tmp_path: Path) -> None:
    malformed_root = make_repository(tmp_path / "malformed")
    state = malformed_root / STATE_DIRECTORY
    state.mkdir(mode=0o700)
    (state / "staged").mkdir(mode=0o700)
    (state / "backups").mkdir(mode=0o700)
    (state / "transaction.json").write_text("not json", encoding="utf-8")
    with pytest.raises(TransactionError, match="malformed"):
        recover_transaction(
            malformed_root,
            manifest_path=MANIFEST,
            validate_predecessor=lambda content, entries: None,
        )

    symlink_root = make_repository(tmp_path / "symlink")
    (symlink_root / STATE_DIRECTORY).symlink_to(state, target_is_directory=True)
    with pytest.raises(TransactionError, match="not a regular directory"):
        recover_transaction(
            symlink_root,
            manifest_path=MANIFEST,
            validate_predecessor=lambda content, entries: None,
        )


def test_transaction_fails_closed_on_windows(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    operations, predecessor = transaction_fixture(root)
    pending = make_repository(tmp_path / "pending-repository")
    (pending / transaction_module.PREPARING_DIRECTORY).mkdir(mode=0o700)
    monkeypatch.setattr(transaction_module.os, "name", "nt")
    with pytest.raises(TransactionError, match="require POSIX"):
        apply_transaction(root, operations, manifest_path=MANIFEST)
    with pytest.raises(TransactionError, match="require POSIX"):
        recover_transaction(pending, manifest_path=MANIFEST, validate_predecessor=lambda content, entries: None)
    assert_predecessor(root, predecessor)
    assert not (root / STATE_DIRECTORY).exists()
    assert (pending / transaction_module.PREPARING_DIRECTORY).exists()


def test_root_lock_rejects_concurrent_transaction(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    operations, predecessor = transaction_fixture(root)
    lock_fd = os.open(root / transaction_module.LOCK_NAME, os.O_RDWR | os.O_CREAT, 0o600)
    try:
        assert transaction_module.fcntl is not None
        transaction_module.fcntl.flock(lock_fd, transaction_module.fcntl.LOCK_EX | transaction_module.fcntl.LOCK_NB)
        with pytest.raises(TransactionError, match="Another DESys transaction"):
            apply_transaction(root, operations, manifest_path=MANIFEST)
    finally:
        os.close(lock_fd)

    assert_predecessor(root, predecessor)
    assert not transaction_module.transaction_pending(root)


@pytest.mark.parametrize(
    ("boundary", "leaves_target"),
    [
        ("after_prepared", False),
        ("after_applying", False),
        ("after_rolling_back", False),
        ("after_restored", False),
        ("after_committed", True),
    ],
)
def test_every_durable_status_transition_is_recoverable(
    tmp_path: Path,
    boundary: str,
    leaves_target: bool,
) -> None:
    root = make_repository(tmp_path / f"repository-{boundary}")
    operations, predecessor = transaction_fixture(root)

    def interrupt(current: str, path: PurePosixPath) -> None:
        if current == boundary:
            raise RuntimeError(f"interrupt {boundary} at {path}")
        if boundary in {"after_rolling_back", "after_restored"} and current == "after_apply" and path == MANIFEST:
            raise RuntimeError("start rollback")

    expected = "cleanup was interrupted|explicit recovery is required" if leaves_target else "restored|explicit recovery"
    with pytest.raises(TransactionError, match=expected):
        apply_transaction(root, operations, manifest_path=MANIFEST, failure_injector=interrupt)

    if leaves_target:
        assert (root / MANIFEST).read_bytes() == b"target manifest\n"
    outcome = None
    if transaction_module.transaction_pending(root):
        outcome = recover_transaction(root, manifest_path=MANIFEST, validate_predecessor=lambda content, entries: None)
    if boundary in {"after_rolling_back", "after_restored"}:
        assert outcome == "restored"
    if boundary == "after_committed":
        assert outcome == "committed"
    if leaves_target:
        assert (root / MANIFEST).read_bytes() == b"target manifest\n"
    else:
        assert_predecessor(root, predecessor)
    assert not transaction_module.transaction_pending(root)


@pytest.mark.parametrize(("boundary", "failure_index"), [
    *(("before_cleanup", index) for index in range(11)),
    *(("after_cleanup", index) for index in range(10)),
])
def test_every_terminal_cleanup_boundary_is_resumable(
    tmp_path: Path,
    boundary: str,
    failure_index: int,
) -> None:
    root = make_repository(tmp_path / f"repository-{boundary}-{failure_index}")
    operations, _ = transaction_fixture(root)
    seen = 0

    def interrupt(current: str, path: PurePosixPath) -> None:
        nonlocal seen
        if current == boundary:
            if seen == failure_index:
                raise RuntimeError(f"cleanup interruption at {path}")
            seen += 1

    with pytest.raises(TransactionError, match="cleanup was interrupted"):
        apply_transaction(root, operations, manifest_path=MANIFEST, failure_injector=interrupt)
    assert transaction_module.transaction_pending(root)

    outcome = recover_transaction(root, manifest_path=MANIFEST, validate_predecessor=lambda content, entries: None)
    assert outcome == "committed"
    assert (root / MANIFEST).read_bytes() == b"target manifest\n"
    assert not transaction_module.transaction_pending(root)


def test_empty_bootstrap_state_is_safely_recoverable(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    (root / transaction_module.PREPARING_DIRECTORY).mkdir(mode=0o700)

    recover_transaction(
        root,
        manifest_path=MANIFEST,
        validate_predecessor=lambda content, entries: pytest.fail("bootstrap must not claim ownership"),
    )

    assert not transaction_module.transaction_pending(root)


def test_predecessor_permission_modes_are_restored_and_preserved(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    operations, predecessor = transaction_fixture(root)
    modes = {
        PurePosixPath("docs/desys/reference/test/update.txt"): 0o640,
        PurePosixPath("docs/desys/reference/test/remove.txt"): 0o600,
        MANIFEST: 0o660,
    }
    for relative, mode in modes.items():
        (root / relative).chmod(mode)

    def fail_after_update(boundary: str, path: PurePosixPath) -> None:
        if boundary == "after_apply" and path.name == "update.txt":
            raise RuntimeError("mode rollback")

    with pytest.raises(TransactionError, match="exact predecessor was restored"):
        apply_transaction(root, operations, manifest_path=MANIFEST, failure_injector=fail_after_update)
    assert_predecessor(root, predecessor)
    assert {relative: stat.S_IMODE((root / relative).stat().st_mode) for relative in modes} == modes

    apply_transaction(root, operations, manifest_path=MANIFEST)
    assert stat.S_IMODE((root / "docs/desys/reference/test/update.txt").stat().st_mode) == 0o640
    assert stat.S_IMODE((root / MANIFEST).stat().st_mode) == 0o660
    assert stat.S_IMODE((root / "docs/desys/reference/test/add.txt").stat().st_mode) == 0o644


def test_cross_filesystem_target_is_rejected_before_state_creation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = make_repository(tmp_path / "repository")
    operations, predecessor = transaction_fixture(root)
    original = transaction_module._read_target

    def wrong_device(root_fd, path, checksum_value, mode=None):
        content, status = original(root_fd, path, checksum_value, mode)
        if path.name == "update.txt":
            status = SimpleNamespace(st_mode=status.st_mode, st_dev=status.st_dev + 1)
        return content, status

    monkeypatch.setattr(transaction_module, "_read_target", wrong_device)
    with pytest.raises(TransactionError, match="another filesystem"):
        apply_transaction(root, operations, manifest_path=MANIFEST)
    assert_predecessor(root, predecessor)
    assert not transaction_module.transaction_pending(root)


def test_hardlinked_target_and_state_content_fail_closed(tmp_path: Path) -> None:
    target_root = make_repository(tmp_path / "target-repository")
    operations, predecessor = transaction_fixture(target_root)
    os.link(target_root / "docs/desys/reference/test/update.txt", target_root / "hardlink")
    with pytest.raises(TransactionError, match="single-link"):
        apply_transaction(target_root, operations, manifest_path=MANIFEST)
    assert_predecessor(target_root, predecessor)

    state_root = make_repository(tmp_path / "state-repository")
    state_operations, _ = transaction_fixture(state_root)

    def interrupt(boundary: str, path: PurePosixPath) -> None:
        if boundary == "after_apply" and path.name == "add.txt":
            raise RuntimeError("apply")
        if boundary == "after_rolling_back":
            raise RuntimeError("rollback")

    with pytest.raises(TransactionError, match="explicit recovery"):
        apply_transaction(state_root, state_operations, manifest_path=MANIFEST, failure_injector=interrupt)
    backup = next((state_root / STATE_DIRECTORY / "backups").iterdir())
    os.link(backup, state_root / "forged-backup-link")
    with pytest.raises(TransactionError, match="single-link|multiple hard links"):
        recover_transaction(state_root, manifest_path=MANIFEST, validate_predecessor=lambda content, entries: None)
    assert transaction_module.transaction_pending(state_root)


def test_forged_executable_mode_is_rejected(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    operations, _ = transaction_fixture(root)

    def interrupt(boundary: str, path: PurePosixPath) -> None:
        if boundary == "after_apply" and path.name == "add.txt":
            raise RuntimeError("apply")
        if boundary == "after_rolling_back":
            raise RuntimeError("rollback")

    with pytest.raises(TransactionError):
        apply_transaction(root, operations, manifest_path=MANIFEST, failure_injector=interrupt)
    record_path = root / STATE_DIRECTORY / "transaction.json"
    record = json.loads(record_path.read_text(encoding="utf-8"))
    record["entries"][0]["after_mode"] = 0o755
    record_path.write_text(json.dumps(record), encoding="utf-8")
    with pytest.raises(TransactionError, match="metadata is malformed"):
        recover_transaction(root, manifest_path=MANIFEST, validate_predecessor=lambda content, entries: None)


def test_symlink_swap_cannot_escape_repository_and_remains_recoverable(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    operations, predecessor = transaction_fixture(root)
    reference = root / "docs/desys/reference"
    moved = root / "docs/desys/reference-original"
    external = tmp_path / "external"
    external.mkdir()
    external_sentinel = external / "sentinel"
    external_sentinel.write_bytes(b"outside\n")
    swapped = False

    def swap(boundary: str, path: PurePosixPath) -> None:
        nonlocal swapped
        if not swapped and boundary == "before_apply" and path.name == "add.txt":
            reference.rename(moved)
            reference.symlink_to(external, target_is_directory=True)
            swapped = True

    with pytest.raises(TransactionError, match="explicit recovery"):
        apply_transaction(root, operations, manifest_path=MANIFEST, failure_injector=swap)
    assert external_sentinel.read_bytes() == b"outside\n"
    assert not (external / "test/add.txt").exists()

    reference.unlink()
    moved.rename(reference)
    recover_transaction(root, manifest_path=MANIFEST, validate_predecessor=lambda content, entries: None)
    assert_predecessor(root, predecessor)


def test_guard_checks_outer_and_inner_git_repositories(tmp_path: Path) -> None:
    outer = make_repository(tmp_path / "outer")
    inner = make_repository(outer / "inner")
    (outer / STATE_DIRECTORY).mkdir()

    with pytest.raises(TransactionError, match="Pending DESys recovery"):
        guard_operation(inner / "docs/file.md")


def test_record_and_executable_prevalidation_happen_before_state_creation(tmp_path: Path) -> None:
    malformed_root = make_repository(tmp_path / "malformed")
    operations, predecessor = transaction_fixture(malformed_root)
    with pytest.raises(TransactionError, match="authenticated path inventory"):
        transaction_module.apply_transaction(
            malformed_root,
            operations,
            authenticate_record=lambda predecessor, target, entries: [],
            manifest_path=MANIFEST,
        )
    assert_predecessor(malformed_root, predecessor)
    assert not transaction_module.transaction_pending(malformed_root)

    executable_root = make_repository(tmp_path / "executable")
    executable_manifest = executable_root / MANIFEST
    executable_manifest.parent.mkdir(parents=True)
    executable_manifest.write_bytes(b"before\n")
    unchanged = PurePosixPath("docs/desys/unchanged.txt")
    (executable_root / unchanged).write_bytes(b"unchanged\n")
    (executable_root / unchanged).chmod(0o755)
    executable_operations = [
        PlannedOperation("UNCHANGED", unchanged, expected_checksum=checksum(b"unchanged\n")),
        PlannedOperation(
            "UPDATE",
            MANIFEST,
            content=b"after\n",
            expected_checksum=checksum(b"before\n"),
            target_checksum=checksum(b"after\n"),
        ),
    ]
    with pytest.raises(TransactionError, match="executable"):
        apply_transaction(executable_root, executable_operations, manifest_path=MANIFEST)
    assert executable_manifest.read_bytes() == b"before\n"
    assert not transaction_module.transaction_pending(executable_root)


def test_addition_publication_link_window_is_recoverable(tmp_path: Path) -> None:
    root = make_repository(tmp_path / "repository")
    operations, predecessor = transaction_fixture(root)
    addition = PurePosixPath("docs/desys/reference/test/add.txt")

    def interrupt(boundary: str, path: PurePosixPath) -> None:
        if boundary == "after_publish_link" and path == addition:
            raise RuntimeError("process stopped between link and unlink")
        if boundary == "after_rolling_back":
            raise RuntimeError("leave durable recovery state")

    with pytest.raises(TransactionError, match="explicit recovery"):
        apply_transaction(root, operations, manifest_path=MANIFEST, failure_injector=interrupt)
    record = json.loads((root / STATE_DIRECTORY / "transaction.json").read_text(encoding="utf-8"))
    entry = next(item for item in record["entries"] if item["path"] == addition.as_posix())
    final = root / addition
    intermediate = final.parent / entry["publish_temp"]
    assert final.stat().st_ino == intermediate.stat().st_ino
    assert final.stat().st_nlink == 2

    recover_transaction(root, manifest_path=MANIFEST, validate_predecessor=lambda content, entries: None)
    assert_predecessor(root, predecessor)
    assert not final.exists()
    assert not intermediate.exists()


@pytest.mark.parametrize("target_name", ["update.txt", "remove.txt"])
def test_final_component_swap_is_captured_without_lost_update(tmp_path: Path, target_name: str) -> None:
    root = make_repository(tmp_path / f"repository-{target_name}")
    operations, predecessor = transaction_fixture(root)
    relative = PurePosixPath(f"docs/desys/reference/test/{target_name}")
    target = root / relative
    attacker_content = b"concurrent replacement\n"
    swapped = False

    def swap(boundary: str, path: PurePosixPath) -> None:
        nonlocal swapped
        if not swapped and boundary == "before_capture" and path == relative:
            target.unlink()
            target.write_bytes(attacker_content)
            swapped = True

    with pytest.raises(TransactionError, match="explicit recovery"):
        apply_transaction(root, operations, manifest_path=MANIFEST, failure_injector=swap)
    record = json.loads((root / STATE_DIRECTORY / "transaction.json").read_text(encoding="utf-8"))
    entry = next(item for item in record["entries"] if item["path"] == relative.as_posix())
    captured = target.parent / entry["before_temp"]
    assert not target.exists()
    assert captured.read_bytes() == attacker_content

    captured.write_bytes(predecessor[relative])
    captured.chmod(entry["before_mode"])
    recover_transaction(root, manifest_path=MANIFEST, validate_predecessor=lambda content, entries: None)
    assert_predecessor(root, predecessor)


@pytest.mark.parametrize("terminal_status", ["committed", "restored"])
def test_forged_partially_cleaned_terminal_record_is_rejected(
    tmp_path: Path,
    terminal_status: str,
) -> None:
    root = make_repository(tmp_path / f"repository-{terminal_status}")
    operations, _ = transaction_fixture(root)
    authorized: list[dict] | None = None

    def authenticate(predecessor: bytes, target: bytes, entries: list[dict]) -> list[dict]:
        nonlocal authorized
        current = authenticate_fixture(predecessor, target, entries)
        if authorized is None:
            authorized = deepcopy(current)
        return deepcopy(authorized)

    cleaned = False

    def interrupt(boundary: str, path: PurePosixPath) -> None:
        nonlocal cleaned
        if terminal_status == "restored" and boundary == "after_apply" and path.name == "update.txt":
            raise RuntimeError("start rollback")
        if boundary == "after_cleanup" and not cleaned:
            cleaned = True
            raise RuntimeError("partial terminal cleanup")

    with pytest.raises(TransactionError, match="cleanup was interrupted|explicit recovery"):
        transaction_module.apply_transaction(
            root,
            operations,
            authenticate_record=authenticate,
            manifest_path=MANIFEST,
            failure_injector=interrupt,
        )
    record_path = root / transaction_module.CLEANUP_DIRECTORY / "transaction.json"
    record = json.loads(record_path.read_text(encoding="utf-8"))
    record["authenticated_paths"][0]["after_checksum"] = checksum(b"forged\n")
    record_path.write_text(json.dumps(record), encoding="utf-8")

    with pytest.raises(TransactionError, match="does not match package evidence"):
        transaction_module.recover_transaction(
            root,
            authenticate_record=authenticate,
            manifest_path=MANIFEST,
        )
    assert transaction_module.transaction_pending(root)


def test_file_mode_is_applied_before_file_fsync(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    directory_fd = os.open(tmp_path, os.O_RDONLY | os.O_DIRECTORY)
    original_fchmod = os.fchmod
    original_fsync = os.fsync
    events: list[tuple[str, int]] = []

    def record_fchmod(descriptor: int, mode: int) -> None:
        events.append(("chmod", descriptor))
        original_fchmod(descriptor, mode)

    def record_fsync(descriptor: int) -> None:
        events.append(("fsync", descriptor))
        original_fsync(descriptor)

    monkeypatch.setattr(transaction_module.os, "fchmod", record_fchmod)
    monkeypatch.setattr(transaction_module.os, "fsync", record_fsync)
    try:
        transaction_module._write_new_at(directory_fd, "content", b"value\n", 0o640)
    finally:
        os.close(directory_fd)

    file_events = [name for name, descriptor in events if descriptor != directory_fd]
    assert file_events == ["chmod", "fsync"]
