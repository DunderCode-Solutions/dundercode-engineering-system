"""Durable, fail-closed POSIX filesystem transactions for DESys migrations."""

from __future__ import annotations

import base64
import hashlib
import json
import os
import secrets
import stat
from collections.abc import Callable, Iterable, Iterator
from contextlib import contextmanager
from pathlib import Path, PurePosixPath
from typing import Literal, Protocol

try:
    import fcntl
except ImportError:  # pragma: no cover - exercised on native Windows CI
    fcntl = None

STATE_DIRECTORY = ".desys-transaction"
PREPARING_DIRECTORY = ".desys-transaction-preparing"
CLEANUP_DIRECTORY = ".desys-transaction-cleanup"
LOCK_NAME = ".desys-transaction.lock"
RECORD_NAME = "transaction.json"
FINAL_RECORD_NAME = ".desys-transaction-final.json"
RECORD_VERSION = 2
STATE_NAMES = (STATE_DIRECTORY, PREPARING_DIRECTORY, CLEANUP_DIRECTORY, FINAL_RECORD_NAME)
FailureInjector = Callable[[str, PurePosixPath], None]
RecordAuthenticator = Callable[[bytes, bytes, list[dict]], list[dict]]
RecoveryOutcome = Literal["restored", "committed"]


class TransactionError(RuntimeError):
    """Raised when transaction state is pending, unsafe, or cannot be recovered."""


class Operation(Protocol):
    action: str
    path: PurePosixPath
    content: bytes | None
    is_directory: bool
    expected_checksum: str | None
    target_checksum: str | None


def transaction_pending(root: Path) -> bool:
    """Return whether any transaction phase directory exists without following it."""
    for name in STATE_NAMES:
        try:
            (root / name).lstat()
        except FileNotFoundError:
            continue
        except OSError:
            return True
        return True
    return False


def require_no_pending_transaction(root: Path) -> None:
    if transaction_pending(root.absolute()):
        raise TransactionError(
            "Pending DESys recovery state exists; run desys-project-init --recover."
        )


def guard_operation(path: Path) -> None:
    """Guard Git worktrees enclosing either the lexical or resolved path."""
    absolute = path.expanduser().absolute()
    try:
        resolved = absolute.resolve(strict=False)
    except (OSError, RuntimeError) as error:
        raise TransactionError(f"Unable to resolve guarded DESys operation path: {error}") from error
    starts = {
        absolute if absolute.is_dir() else absolute.parent,
        resolved if resolved.is_dir() else resolved.parent,
    }
    repositories = {
        candidate
        for start in starts
        for candidate in (start, *start.parents)
        if (candidate / ".git").exists() or (candidate / ".git").is_symlink()
    }
    for repository in repositories:
        require_no_pending_transaction(repository)


def apply_transaction(
    root: Path,
    operations: Iterable[Operation],
    *,
    authenticate_record: RecordAuthenticator,
    manifest_path: PurePosixPath,
    failure_injector: FailureInjector | None = None,
) -> None:
    """Stage and apply operations, restoring the predecessor on apply failure."""
    _require_transaction_platform()
    root = root.resolve(strict=True)
    all_operations = tuple(operations)
    changed = sorted(
        (
            operation
            for operation in all_operations
            if operation.action in {"ADD", "CREATE", "UPDATE", "REMOVE", "DELETE"}
            and not operation.is_directory
        ),
        key=lambda item: (item.path == manifest_path, item.path.as_posix()),
    )
    if not changed:
        return
    if changed[-1].path != manifest_path:
        raise TransactionError("A migration transaction must publish the target manifest last.")

    with _locked_root(root) as root_fd:
        require_no_pending_transaction(root)
        root_device = os.fstat(root_fd).st_dev
        _prevalidate_managed_files(root_fd, all_operations, root_device)
        directories = _created_directories(root_fd, all_operations, changed, root_device)
        transaction_id = secrets.token_hex(16)
        entries = [
            _entry_for(root_fd, operation, index, root_device, transaction_id)
            for index, operation in enumerate(changed)
        ]
        manifest_operation = changed[-1]
        predecessor_manifest, _ = _read_target(
            root_fd,
            manifest_path,
            manifest_operation.expected_checksum,
        )
        if manifest_operation.content is None:
            raise TransactionError("A migration transaction requires target manifest content.")
        predecessor_evidence = _encode_evidence(predecessor_manifest)
        target_evidence = _encode_evidence(manifest_operation.content)
        authenticated_paths = authenticate_record(predecessor_manifest, manifest_operation.content, entries)
        record = {
            "transaction_version": RECORD_VERSION,
            "transaction_id": transaction_id,
            "status": "preparing",
            "root_device": root_device,
            "predecessor_manifest": predecessor_evidence,
            "target_manifest": target_evidence,
            "authenticated_paths": authenticated_paths,
            "created_directories": [path.as_posix() for path in directories],
            "entries": entries,
        }
        _validate_record(record, PREPARING_DIRECTORY)
        _authenticate_record(record, authenticate_record)
        phase = PREPARING_DIRECTORY
        try:
            _create_state(root_fd, phase, record)
            _stage(root_fd, phase, changed, entries, failure_injector)
            record["status"] = "prepared"
            _write_record(root_fd, phase, record)
            _inject(failure_injector, "after_prepared", manifest_path)
            _rename_at(root_fd, phase, STATE_DIRECTORY)
            phase = STATE_DIRECTORY
            record["status"] = "applying"
            _write_record(root_fd, phase, record)
            _inject(failure_injector, "after_applying", manifest_path)
            for relative in directories:
                _inject(failure_injector, "before_apply", relative)
                _mkdir_at(root_fd, relative)
                _inject(failure_injector, "after_apply", relative)
            for operation, entry in zip(changed, entries, strict=True):
                _inject(failure_injector, "before_apply", operation.path)
                _apply_entry(root_fd, phase, entry, failure_injector)
                _inject(failure_injector, "after_apply", operation.path)
            _verify_tree(root_fd, entries, directories, predecessor=False)
            _verify_authenticated_paths(root_fd, authenticated_paths, predecessor=False)
            record["status"] = "committed"
            _write_record(root_fd, phase, record)
            _inject(failure_injector, "after_committed", manifest_path)
            _terminal_cleanup(root_fd, phase, record, failure_injector)
        except Exception as apply_error:
            try:
                existing = _existing_states_fd(root_fd)
                if CLEANUP_DIRECTORY in existing or _name_exists(root_fd, FINAL_RECORD_NAME):
                    raise TransactionError(
                        "Migration reached a durable terminal state but cleanup was interrupted; "
                        "explicit recovery is required."
                    ) from apply_error
                if PREPARING_DIRECTORY in existing:
                    loaded = _load_record(root_fd, PREPARING_DIRECTORY, allow_empty=True)
                    if loaded is None:
                        _remove_empty_state(root_fd, PREPARING_DIRECTORY)
                    else:
                        _verify_tree(
                            root_fd,
                            loaded["entries"],
                            _record_directories(loaded),
                            predecessor=True,
                        )
                        _verify_authenticated_paths(root_fd, loaded["authenticated_paths"], predecessor=True)
                        loaded["status"] = "restored"
                        _write_record(root_fd, PREPARING_DIRECTORY, loaded)
                        _terminal_cleanup(root_fd, PREPARING_DIRECTORY, loaded, failure_injector)
                elif STATE_DIRECTORY in existing:
                    loaded = _load_record(root_fd, STATE_DIRECTORY)
                    if loaded["status"] == "committed":
                        raise TransactionError(
                            "Migration committed but cleanup was interrupted; explicit recovery is required."
                        ) from apply_error
                    _rollback(root_fd, STATE_DIRECTORY, loaded, failure_injector)
            except Exception as rollback_error:
                if isinstance(rollback_error, TransactionError) and "cleanup was interrupted" in str(rollback_error):
                    raise
                raise TransactionError(
                    f"Migration failed and rollback was interrupted; explicit recovery is required: {rollback_error}"
                ) from apply_error
            raise TransactionError(f"Migration failed; the exact predecessor was restored: {apply_error}") from apply_error


def recover_transaction(
    root: Path,
    *,
    authenticate_record: RecordAuthenticator,
    manifest_path: PurePosixPath,
    failure_injector: FailureInjector | None = None,
) -> RecoveryOutcome:
    """Recover or finish cleanup for the sole durable transaction state."""
    _require_transaction_platform()
    root = root.resolve(strict=True)
    with _locked_root(root) as root_fd:
        states = _existing_states_fd(root_fd)
        final_record_exists = _name_exists(root_fd, FINAL_RECORD_NAME)
        if final_record_exists:
            if states not in ([], [CLEANUP_DIRECTORY]):
                raise TransactionError("Final transaction record conflicts with another transaction phase.")
            record = _load_final_record(root_fd)
            _authenticate_record(record, authenticate_record)
            predecessor = record["status"] == "restored"
            _verify_tree(root_fd, record["entries"], _record_directories(record), predecessor=predecessor)
            _verify_authenticated_paths(root_fd, record["authenticated_paths"], predecessor=predecessor)
            if states:
                _remove_empty_state(root_fd, CLEANUP_DIRECTORY)
            _unlink_name(root_fd, FINAL_RECORD_NAME)
            return "restored" if predecessor else "committed"
        if len(states) != 1:
            raise TransactionError("Recovery requires exactly one transaction phase directory.")
        phase = states[0]
        if phase == CLEANUP_DIRECTORY:
            record = _load_record(root_fd, phase, allow_empty=True)
            if record is None:
                _remove_empty_state(root_fd, phase)
                return "restored"
            _authenticate_record(record, authenticate_record)
            predecessor = record["status"] == "restored"
            _verify_tree(root_fd, record["entries"], _record_directories(record), predecessor=predecessor)
            _verify_authenticated_paths(root_fd, record["authenticated_paths"], predecessor=predecessor)
            _cleanup_state(root_fd, phase, record, failure_injector)
            return "restored" if predecessor else "committed"

        record = _load_record(root_fd, phase, allow_empty=phase == PREPARING_DIRECTORY)
        if record is None:
            _remove_empty_state(root_fd, phase)
            return "restored"
        _authenticate_record(record, authenticate_record)
        if phase == PREPARING_DIRECTORY or record["status"] == "prepared":
            _verify_tree(root_fd, record["entries"], _record_directories(record), predecessor=True)
            _verify_authenticated_paths(root_fd, record["authenticated_paths"], predecessor=True)
            record["status"] = "restored"
            _write_record(root_fd, phase, record)
            _terminal_cleanup(root_fd, phase, record, failure_injector)
            return "restored"
        if record["status"] in {"restored", "committed"}:
            predecessor = record["status"] == "restored"
            _verify_tree(root_fd, record["entries"], _record_directories(record), predecessor=predecessor)
            _verify_authenticated_paths(root_fd, record["authenticated_paths"], predecessor=predecessor)
            _terminal_cleanup(root_fd, phase, record, failure_injector)
            return "restored" if predecessor else "committed"
        _rollback(root_fd, phase, record, failure_injector)
        return "restored"


def _require_transaction_platform() -> None:
    required_dir_fd = {os.open, os.mkdir, os.rename, os.stat, os.unlink, os.rmdir, os.link}
    if (
        os.name != "posix"
        or not hasattr(os, "O_NOFOLLOW")
        or not hasattr(os, "O_DIRECTORY")
        or not required_dir_fd.issubset(os.supports_dir_fd)
    ):
        raise TransactionError(
            "Transactional migration apply and recovery require POSIX dir_fd, O_NOFOLLOW, directory fsync, and flock."
        )
    if fcntl is None:
        raise TransactionError("Transactional migration requires POSIX flock support.")


@contextmanager
def _locked_root(root: Path) -> Iterator[int]:
    if fcntl is None:
        raise TransactionError("Transactional migration requires POSIX flock support.")
    root_fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    lock_fd = -1
    try:
        lock_fd = os.open(LOCK_NAME, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600, dir_fd=root_fd)
        lock_status = os.fstat(lock_fd)
        if not stat.S_ISREG(lock_status.st_mode) or lock_status.st_nlink != 1:
            raise TransactionError("Transaction lock is not a regular single-link file.")
        os.fchmod(lock_fd, 0o600)
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise TransactionError("Another DESys transaction or recovery is active.") from error
        yield root_fd
    finally:
        if lock_fd >= 0:
            os.close(lock_fd)
        os.close(root_fd)


def _entry_for(
    root_fd: int,
    operation: Operation,
    index: int,
    root_device: int,
    transaction_id: str,
) -> dict[str, object]:
    path = _safe_relative(operation.path.as_posix())
    before = operation.expected_checksum
    after = operation.target_checksum
    if operation.action in {"ADD", "CREATE"}:
        before = None
    if operation.action in {"REMOVE", "DELETE"}:
        after = None
    elif operation.content is not None:
        calculated = _checksum(operation.content)
        if after is not None and after != calculated:
            raise TransactionError(f"Target checksum is inconsistent for {path}.")
        after = calculated

    before_mode: int | None = None
    if before is not None:
        _, status = _read_target(root_fd, path, before)
        before_mode = stat.S_IMODE(status.st_mode)
        if before_mode & 0o111:
            raise TransactionError(f"Managed predecessor file is executable: {path}")
        if status.st_dev != root_device:
            raise TransactionError(f"Managed target is on another filesystem: {path}")
    elif _target_exists(root_fd, path):
        raise TransactionError(f"Migration addition became occupied: {path}")
    parent_fd = _open_nearest_existing_directory(root_fd, path.parent)
    try:
        if os.fstat(parent_fd).st_dev != root_device:
            raise TransactionError(f"Managed target parent is on another filesystem: {path.parent}")
    finally:
        os.close(parent_fd)
    after_mode = None if after is None else (before_mode if before_mode is not None else 0o644)
    return {
        "path": path.as_posix(),
        "before_checksum": before,
        "after_checksum": after,
        "before_mode": before_mode,
        "after_mode": after_mode,
        "backup": f"{index:04d}.bin" if before is not None else None,
        "staged": f"{index:04d}.bin" if after is not None else None,
        "before_temp": f".desys-{transaction_id}-{index:04d}-before" if before is not None else None,
        "publish_temp": f".desys-{transaction_id}-{index:04d}-publish" if after is not None else None,
    }


def _created_directories(
    root_fd: int,
    operations: tuple[Operation, ...],
    changed: list[Operation],
    root_device: int,
) -> list[PurePosixPath]:
    candidates = {
        operation.path
        for operation in operations
        if operation.is_directory and operation.action == "CREATE"
    }
    for operation in changed:
        candidates.update(parent for parent in operation.path.parents if parent != PurePosixPath("."))
    missing: set[PurePosixPath] = set()
    for relative in sorted(candidates, key=lambda path: (len(path.parts), path.as_posix())):
        relative = _safe_relative(relative.as_posix())
        try:
            descriptor = _open_directory(root_fd, relative)
        except FileNotFoundError:
            missing.add(relative)
            continue
        except OSError as error:
            raise TransactionError(f"Unsafe managed directory {relative}: {error}") from error
        try:
            if os.fstat(descriptor).st_dev != root_device:
                raise TransactionError(f"Managed directory is on another filesystem: {relative}")
        finally:
            os.close(descriptor)
    for relative in missing:
        existing = next((parent for parent in relative.parents if parent not in missing and parent != PurePosixPath(".")), None)
        descriptor = root_fd if existing is None else _open_directory(root_fd, existing)
        try:
            if os.fstat(descriptor).st_dev != root_device:
                raise TransactionError(f"Managed directory parent is on another filesystem: {relative}")
        finally:
            if descriptor != root_fd:
                os.close(descriptor)
    return sorted(missing, key=lambda path: (len(path.parts), path.as_posix()))


def _prevalidate_managed_files(
    root_fd: int,
    operations: tuple[Operation, ...],
    root_device: int,
) -> None:
    for operation in operations:
        if operation.is_directory or operation.expected_checksum is None:
            continue
        path = _safe_relative(operation.path.as_posix())
        _, status = _read_target(root_fd, path, operation.expected_checksum)
        mode = stat.S_IMODE(status.st_mode)
        if mode & 0o111:
            raise TransactionError(f"Managed predecessor file is executable: {path}")
        if status.st_dev != root_device:
            raise TransactionError(f"Managed target is on another filesystem: {path}")


def _create_state(root_fd: int, phase: str, record: dict) -> None:
    os.mkdir(phase, 0o700, dir_fd=root_fd)
    _fsync_fd(root_fd)
    _write_record(root_fd, phase, record)
    state_fd = _open_directory(root_fd, PurePosixPath(phase))
    try:
        os.mkdir("staged", 0o700, dir_fd=state_fd)
        os.mkdir("backups", 0o700, dir_fd=state_fd)
        _fsync_fd(state_fd)
    finally:
        os.close(state_fd)


def _stage(
    root_fd: int,
    phase: str,
    operations: list[Operation],
    entries: list[dict],
    injector: FailureInjector | None,
) -> None:
    state_fd = _open_directory(root_fd, PurePosixPath(phase))
    staged_fd = _open_directory(state_fd, PurePosixPath("staged"))
    backups_fd = _open_directory(state_fd, PurePosixPath("backups"))
    try:
        state_device = os.fstat(state_fd).st_dev
        for operation, entry in zip(operations, entries, strict=True):
            _inject(injector, "before_stage", operation.path)
            if operation.content is not None:
                _write_new_at(staged_fd, entry["staged"], operation.content, 0o600)
            if entry["before_checksum"] is not None:
                content, status = _read_target(root_fd, operation.path, entry["before_checksum"])
                if status.st_dev != state_device:
                    raise TransactionError(f"Backup staging crosses filesystems: {operation.path}")
                _write_new_at(backups_fd, entry["backup"], content, 0o600)
            _inject(injector, "after_stage", operation.path)
        _fsync_fd(staged_fd)
        _fsync_fd(backups_fd)
    finally:
        os.close(backups_fd)
        os.close(staged_fd)
        os.close(state_fd)


def _apply_entry(
    root_fd: int,
    phase: str,
    entry: dict,
    injector: FailureInjector | None,
) -> None:
    path = _safe_relative(entry["path"])
    before = entry["before_checksum"]
    after = entry["after_checksum"]
    parent_fd = _open_parent(root_fd, path)
    try:
        if after is not None:
            content = _read_state_content(root_fd, phase, "staged", entry["staged"], after)
            _write_new_at(parent_fd, entry["publish_temp"], content, entry["after_mode"])
        if before is not None:
            _inject(injector, "before_capture", path)
            _capture_name(parent_fd, path.name, entry["before_temp"])
            _read_named_target(
                parent_fd,
                entry["before_temp"],
                before,
                entry["before_mode"],
            )
            _inject(injector, "after_capture", path)
        if after is not None:
            _publish_name(parent_fd, entry["publish_temp"], path.name, injector, path)
        if before is not None:
            _unlink_name(parent_fd, entry["before_temp"])
    finally:
        os.close(parent_fd)


def _rollback(root_fd: int, phase: str, record: dict, injector: FailureInjector | None) -> None:
    if record["status"] not in {"prepared", "applying", "rolling_back"}:
        raise TransactionError(f"Transaction status cannot be rolled back: {record['status']}")
    record["status"] = "rolling_back"
    _write_record(root_fd, phase, record)
    _inject(injector, "after_rolling_back", PurePosixPath(RECORD_NAME))
    for entry in reversed(record["entries"]):
        path = _safe_relative(entry["path"])
        _inject(injector, "before_rollback", path)
        _rollback_entry(root_fd, phase, entry, injector)
        _inject(injector, "after_rollback", path)
    for relative in reversed(_record_directories(record)):
        _inject(injector, "before_rollback", relative)
        if _directory_exists(root_fd, relative):
            _rmdir_at(root_fd, relative)
        _inject(injector, "after_rollback", relative)
    _verify_tree(root_fd, record["entries"], _record_directories(record), predecessor=True)
    _verify_authenticated_paths(root_fd, record["authenticated_paths"], predecessor=True)
    record["status"] = "restored"
    _write_record(root_fd, phase, record)
    _inject(injector, "after_restored", PurePosixPath(RECORD_NAME))
    _terminal_cleanup(root_fd, phase, record, injector)


def _rollback_entry(
    root_fd: int,
    phase: str,
    entry: dict,
    injector: FailureInjector | None,
) -> None:
    path = _safe_relative(entry["path"])
    before = entry["before_checksum"]
    after = entry["after_checksum"]
    parent_fd = _open_parent(root_fd, path)
    try:
        if before is None:
            _remove_recognized_name(parent_fd, path.name, after, entry["after_mode"])
            _remove_recognized_name(parent_fd, entry["publish_temp"], after, entry["after_mode"])
            return

        backup = _read_state_content(root_fd, phase, "backups", entry["backup"], before)
        before_temp = entry["before_temp"]
        if _name_exists(parent_fd, before_temp):
            _read_named_target(parent_fd, before_temp, before, entry["before_mode"], allow_two_links=True)
        elif _name_exists(parent_fd, path.name):
            current, status = _read_named_target(parent_fd, path.name, None, None, allow_two_links=True)
            current_checksum = _checksum(current)
            current_mode = stat.S_IMODE(status.st_mode)
            if current_checksum == before and current_mode == entry["before_mode"]:
                _remove_recognized_name(parent_fd, entry["publish_temp"], after, entry["after_mode"])
                return
            if current_checksum != after or current_mode != entry["after_mode"]:
                raise TransactionError(f"Recovery target has unrecognized bytes or permissions: {path}")
            _capture_name(parent_fd, path.name, before_temp)
            _read_named_target(parent_fd, before_temp, after, entry["after_mode"])
            _unlink_name(parent_fd, before_temp)

        _remove_recognized_name(parent_fd, entry["publish_temp"], after, entry["after_mode"])
        if not _name_exists(parent_fd, before_temp):
            _write_new_at(parent_fd, before_temp, backup, entry["before_mode"])
        _read_named_target(parent_fd, before_temp, before, entry["before_mode"], allow_two_links=True)
        if _name_exists(parent_fd, path.name):
            final_content, final_status = _read_named_target(parent_fd, path.name, None, None, allow_two_links=True)
            final_checksum = _checksum(final_content)
            final_mode = stat.S_IMODE(final_status.st_mode)
            if final_checksum == before and final_mode == entry["before_mode"]:
                _unlink_name(parent_fd, before_temp)
                return
            if final_checksum != after or final_mode != entry["after_mode"]:
                raise TransactionError(f"Recovery target is not a recognized transaction version: {path}")
            _unlink_name(parent_fd, path.name)
        _publish_name(parent_fd, before_temp, path.name, injector, path)
    finally:
        os.close(parent_fd)


def _terminal_cleanup(root_fd: int, phase: str, record: dict, injector: FailureInjector | None) -> None:
    if record["status"] not in {"committed", "restored"}:
        raise TransactionError("Only a verified terminal transaction can be cleaned up.")
    if phase != CLEANUP_DIRECTORY:
        _rename_at(root_fd, phase, CLEANUP_DIRECTORY)
        phase = CLEANUP_DIRECTORY
    _cleanup_state(root_fd, phase, record, injector)


def _cleanup_state(root_fd: int, phase: str, record: dict, injector: FailureInjector | None) -> None:
    state_fd = _open_directory(root_fd, PurePosixPath(phase))
    try:
        for directory_name, field in (("staged", "staged"), ("backups", "backup")):
            if directory_name not in os.listdir(state_fd):
                continue
            directory_fd = _open_directory(state_fd, PurePosixPath(directory_name))
            try:
                expected = {entry[field] for entry in record["entries"] if entry[field] is not None}
                actual = set(os.listdir(directory_fd))
                if not actual.issubset(expected):
                    raise TransactionError("Terminal cleanup contains forged transaction content.")
                for name in sorted(actual):
                    _inject(injector, "before_cleanup", PurePosixPath(directory_name) / name)
                    _unlink_name(directory_fd, name)
                    _inject(injector, "after_cleanup", PurePosixPath(directory_name) / name)
            finally:
                os.close(directory_fd)
            _inject(injector, "before_cleanup", PurePosixPath(directory_name))
            os.rmdir(directory_name, dir_fd=state_fd)
            _fsync_fd(state_fd)
            _inject(injector, "after_cleanup", PurePosixPath(directory_name))
        names = set(os.listdir(state_fd))
        if names != {RECORD_NAME}:
            raise TransactionError("Terminal transaction state contains unexpected entries.")
        _inject(injector, "before_cleanup", PurePosixPath(RECORD_NAME))
        if _name_exists(root_fd, FINAL_RECORD_NAME):
            raise TransactionError("Final transaction record is already occupied.")
        os.rename(RECORD_NAME, FINAL_RECORD_NAME, src_dir_fd=state_fd, dst_dir_fd=root_fd)
        _fsync_fd(state_fd)
        _fsync_fd(root_fd)
        _inject(injector, "after_cleanup", PurePosixPath(RECORD_NAME))
    finally:
        os.close(state_fd)
    _inject(injector, "before_cleanup", PurePosixPath(phase))
    os.rmdir(phase, dir_fd=root_fd)
    _fsync_fd(root_fd)
    _inject(injector, "after_cleanup", PurePosixPath(phase))
    _inject(injector, "before_cleanup", PurePosixPath(FINAL_RECORD_NAME))
    _unlink_name(root_fd, FINAL_RECORD_NAME)


def _remove_empty_state(root_fd: int, phase: str) -> None:
    state_fd = _open_directory(root_fd, PurePosixPath(phase))
    try:
        if os.listdir(state_fd):
            raise TransactionError("Recordless transaction state is not empty.")
    finally:
        os.close(state_fd)
    os.rmdir(phase, dir_fd=root_fd)
    _fsync_fd(root_fd)


def _load_record(root_fd: int, phase: str, *, allow_empty: bool = False) -> dict | None:
    state_fd = _open_directory(root_fd, PurePosixPath(phase))
    try:
        state_status = os.fstat(state_fd)
        if stat.S_IMODE(state_status.st_mode) & 0o077:
            raise TransactionError("Transaction state directory permissions are unsafe.")
        names = set(os.listdir(state_fd))
        if allow_empty and not names:
            return None
        expected_root_names = {RECORD_NAME, "staged", "backups"}
        if phase in {CLEANUP_DIRECTORY, PREPARING_DIRECTORY}:
            valid_names = RECORD_NAME in names and names.issubset(expected_root_names)
        else:
            valid_names = names == expected_root_names
        if not valid_names:
            raise TransactionError("Transaction state contains unexpected entries.")
        content, record_status = _read_file_at(state_fd, RECORD_NAME)
        if record_status.st_nlink != 1:
            raise TransactionError("Transaction record has multiple hard links.")
        try:
            record = json.loads(content)
        except (UnicodeError, json.JSONDecodeError) as error:
            raise TransactionError(f"Transaction record is malformed: {error}") from error
        _validate_record(record, phase)
        if record["root_device"] != os.fstat(root_fd).st_dev or state_status.st_dev != record["root_device"]:
            raise TransactionError("Transaction state is on an unexpected filesystem.")
        complete = record["status"] != "preparing"
        for directory_name, field, checksum_field in (
            ("staged", "staged", "after_checksum"),
            ("backups", "backup", "before_checksum"),
        ):
            if directory_name not in names:
                if phase == CLEANUP_DIRECTORY:
                    continue
                if not complete:
                    continue
                raise TransactionError("Transaction content directory is missing.")
            directory_fd = _open_directory(state_fd, PurePosixPath(directory_name))
            try:
                status = os.fstat(directory_fd)
                if stat.S_IMODE(status.st_mode) & 0o077:
                    raise TransactionError("Transaction content directory permissions are unsafe.")
                expected = {entry[field] for entry in record["entries"] if entry[field] is not None}
                actual = set(os.listdir(directory_fd))
                if (
                    phase == CLEANUP_DIRECTORY
                    and not actual.issubset(expected)
                    or phase != CLEANUP_DIRECTORY
                    and complete
                    and actual != expected
                    or not complete
                    and not actual.issubset(expected)
                ):
                    raise TransactionError("Transaction content set is inconsistent.")
                for entry in record["entries"]:
                    name = entry[field]
                    if name in actual:
                        _, content_status = _read_file_at(directory_fd, name, entry[checksum_field])
                        if content_status.st_nlink != 1:
                            raise TransactionError("Transaction content has multiple hard links.")
            finally:
                os.close(directory_fd)
        return record
    finally:
        os.close(state_fd)


def _load_final_record(root_fd: int) -> dict:
    content, status = _read_file_at(root_fd, FINAL_RECORD_NAME)
    if status.st_nlink != 1 or stat.S_IMODE(status.st_mode) & 0o077:
        raise TransactionError("Final transaction record permissions or links are unsafe.")
    try:
        record = json.loads(content)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise TransactionError(f"Final transaction record is malformed: {error}") from error
    _validate_record(record, CLEANUP_DIRECTORY)
    if record["root_device"] != os.fstat(root_fd).st_dev:
        raise TransactionError("Final transaction record is on an unexpected filesystem.")
    return record


def _validate_record(record: object, phase: str) -> None:
    fields = {
        "transaction_version",
        "transaction_id",
        "status",
        "root_device",
        "predecessor_manifest",
        "target_manifest",
        "authenticated_paths",
        "created_directories",
        "entries",
    }
    if not isinstance(record, dict) or set(record) != fields:
        raise TransactionError("Transaction record fields are malformed.")
    statuses = {
        PREPARING_DIRECTORY: {"preparing", "prepared", "restored"},
        STATE_DIRECTORY: {"prepared", "applying", "rolling_back", "restored", "committed"},
        CLEANUP_DIRECTORY: {"restored", "committed"},
    }
    if record["transaction_version"] != RECORD_VERSION or record["status"] not in statuses[phase]:
        raise TransactionError("Transaction record version, phase, or status is unsupported.")
    if type(record["root_device"]) is not int or record["root_device"] < 0:
        raise TransactionError("Transaction root device is malformed.")
    transaction_id = record["transaction_id"]
    if (
        not isinstance(transaction_id, str)
        or len(transaction_id) != 32
        or any(character not in "0123456789abcdef" for character in transaction_id)
    ):
        raise TransactionError("Transaction identifier is malformed.")
    predecessor_manifest = _decode_evidence(record["predecessor_manifest"])
    target_manifest = _decode_evidence(record["target_manifest"])
    if not isinstance(record["entries"], list) or not record["entries"]:
        raise TransactionError("Transaction record entries are malformed.")
    seen: set[str] = set()
    for index, entry in enumerate(record["entries"]):
        _validate_entry(entry, seen, transaction_id, index)
    authenticated_paths = record["authenticated_paths"]
    if not isinstance(authenticated_paths, list) or not authenticated_paths:
        raise TransactionError("Transaction authenticated path inventory is malformed.")
    inventory_paths: list[str] = []
    for item in authenticated_paths:
        if not isinstance(item, dict) or set(item) != {"path", "before_checksum", "after_checksum"}:
            raise TransactionError("Transaction authenticated path inventory is malformed.")
        path = _safe_relative(item["path"]).as_posix()
        for field in ("before_checksum", "after_checksum"):
            value = item[field]
            if value is not None and (not isinstance(value, str) or not _valid_checksum(value)):
                raise TransactionError("Transaction authenticated checksum inventory is malformed.")
        if item["before_checksum"] is None and item["after_checksum"] is None:
            raise TransactionError("Transaction authenticated path has no state.")
        inventory_paths.append(path)
    if inventory_paths != sorted(set(inventory_paths)):
        raise TransactionError("Transaction authenticated paths are not unique and ordered.")
    if record["entries"][-1]["path"] != "docs/desys/corpus-manifest.yaml":
        raise TransactionError("Transaction record does not publish the manifest last.")
    manifest_entry = record["entries"][-1]
    if (
        _checksum(predecessor_manifest) != manifest_entry["before_checksum"]
        or _checksum(target_manifest) != manifest_entry["after_checksum"]
    ):
        raise TransactionError("Transaction manifest evidence does not match the recorded transition.")
    directories = _record_directories(record)
    entry_paths = [_safe_relative(entry["path"]) for entry in record["entries"]]
    if any(not any(directory in path.parents for path in entry_paths) for directory in directories):
        raise TransactionError("Transaction record contains an unrelated directory.")


def _validate_entry(entry: object, seen: set[str], transaction_id: str, index: int) -> None:
    fields = {
        "path",
        "before_checksum",
        "after_checksum",
        "before_mode",
        "after_mode",
        "backup",
        "staged",
        "before_temp",
        "publish_temp",
    }
    if not isinstance(entry, dict) or set(entry) != fields:
        raise TransactionError("Transaction record entry fields are malformed.")
    path = _safe_relative(entry["path"])
    if path.as_posix() in seen:
        raise TransactionError("Transaction record contains duplicate paths.")
    seen.add(path.as_posix())
    for checksum_field, mode_field, content_field in (
        ("before_checksum", "before_mode", "backup"),
        ("after_checksum", "after_mode", "staged"),
    ):
        checksum = entry[checksum_field]
        mode = entry[mode_field]
        name = entry[content_field]
        if checksum is None:
            if mode is not None or name is not None:
                raise TransactionError("Transaction record metadata is inconsistent.")
        elif (
            not isinstance(checksum, str)
            or not _valid_checksum(checksum)
            or type(mode) is not int
            or not 0 <= mode <= 0o7777
            or not isinstance(name, str)
            or not name.endswith(".bin")
            or "/" in name
            or mode & 0o111
        ):
            raise TransactionError("Transaction record metadata is malformed.")
    if (
        entry["before_mode"] is not None
        and entry["after_mode"] is not None
        and entry["before_mode"] != entry["after_mode"]
    ):
        raise TransactionError("Transaction update permissions are inconsistent.")
    expected_before_temp = (
        f".desys-{transaction_id}-{index:04d}-before" if entry["before_checksum"] is not None else None
    )
    expected_publish_temp = (
        f".desys-{transaction_id}-{index:04d}-publish" if entry["after_checksum"] is not None else None
    )
    if entry["before_temp"] != expected_before_temp or entry["publish_temp"] != expected_publish_temp:
        raise TransactionError("Transaction mutation intermediates are malformed.")


def _authenticate_record(record: dict, authenticator: RecordAuthenticator) -> None:
    try:
        authenticated_paths = authenticator(
            _decode_evidence(record["predecessor_manifest"]),
            _decode_evidence(record["target_manifest"]),
            record["entries"],
        )
        if authenticated_paths != record["authenticated_paths"]:
            raise TransactionError("Transaction authenticated path inventory does not match package evidence.")
    except TransactionError:
        raise
    except Exception as error:
        raise TransactionError(f"Transaction record authentication failed: {error}") from error


def _verify_tree(
    root_fd: int,
    entries: list[dict],
    directories: list[PurePosixPath],
    *,
    predecessor: bool,
) -> None:
    checksum_field = "before_checksum" if predecessor else "after_checksum"
    mode_field = "before_mode" if predecessor else "after_mode"
    for entry in entries:
        path = _safe_relative(entry["path"])
        expected = entry[checksum_field]
        if expected is None:
            if _target_exists(root_fd, path):
                raise TransactionError(f"Transaction verification found an unexpected path: {path}")
        else:
            _read_target(root_fd, path, expected, entry[mode_field])
        try:
            parent_fd = _open_parent(root_fd, path)
        except TransactionError as error:
            if predecessor and expected is None and isinstance(error.__cause__, FileNotFoundError):
                continue
            raise
        try:
            for field in ("before_temp", "publish_temp"):
                name = entry[field]
                if name is not None and _name_exists(parent_fd, name):
                    raise TransactionError(f"Transaction verification found an intermediate path: {name}")
        finally:
            os.close(parent_fd)
    for relative in directories:
        exists = _directory_exists(root_fd, relative)
        if predecessor and exists:
            raise TransactionError(f"Predecessor verification found an added directory: {relative}")
        if not predecessor and not exists:
            raise TransactionError(f"Target verification found a missing directory: {relative}")


def _verify_authenticated_paths(
    root_fd: int,
    paths: list[dict],
    *,
    predecessor: bool,
) -> None:
    field = "before_checksum" if predecessor else "after_checksum"
    for item in paths:
        path = _safe_relative(item["path"])
        expected = item[field]
        if expected is None:
            if _target_exists(root_fd, path):
                raise TransactionError(f"Authenticated transaction tree contains an unexpected path: {path}")
        else:
            _, status = _read_target(root_fd, path, expected)
            if stat.S_IMODE(status.st_mode) & 0o111:
                raise TransactionError(f"Authenticated managed file is executable: {path}")


def _write_record(root_fd: int, phase: str, record: dict) -> None:
    state_fd = _open_directory(root_fd, PurePosixPath(phase))
    try:
        content = (json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n").encode()
        _atomic_write_name(state_fd, RECORD_NAME, content, 0o600)
    finally:
        os.close(state_fd)


def _read_state_content(
    root_fd: int,
    phase: str,
    directory: str,
    name: str,
    checksum: str,
) -> bytes:
    state_fd = _open_directory(root_fd, PurePosixPath(phase))
    directory_fd = _open_directory(state_fd, PurePosixPath(directory))
    try:
        content, status = _read_file_at(directory_fd, name, checksum)
        if status.st_nlink != 1:
            raise TransactionError("Transaction content has multiple hard links.")
        return content
    finally:
        os.close(directory_fd)
        os.close(state_fd)


def _read_target(
    root_fd: int,
    path: PurePosixPath,
    checksum: str | None,
    mode: int | None = None,
) -> tuple[bytes, os.stat_result]:
    parent_fd = _open_parent(root_fd, path)
    try:
        content, status = _read_file_at(parent_fd, path.name, checksum)
    finally:
        os.close(parent_fd)
    if mode is not None and stat.S_IMODE(status.st_mode) != mode:
        raise TransactionError(f"Transaction permission mismatch: {path}")
    return content, status


def _read_named_target(
    directory_fd: int,
    name: str,
    checksum: str | None,
    mode: int | None,
    *,
    allow_two_links: bool = False,
) -> tuple[bytes, os.stat_result]:
    descriptor = -1
    try:
        descriptor = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory_fd)
        status = os.fstat(descriptor)
        allowed_links = {1, 2} if allow_two_links else {1}
        if not stat.S_ISREG(status.st_mode) or status.st_nlink not in allowed_links:
            raise TransactionError(f"Transaction path has unsafe type or link count: {name}")
        if mode is not None and stat.S_IMODE(status.st_mode) != mode:
            raise TransactionError(f"Transaction permission mismatch: {name}")
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = -1
            content = stream.read()
    except OSError as error:
        raise TransactionError(f"Unable to read transaction target {name}: {error}") from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    if checksum is not None and _checksum(content) != checksum:
        raise TransactionError(f"Transaction checksum mismatch: {name}")
    return content, status


def _read_file_at(directory_fd: int, name: str, checksum: str | None = None) -> tuple[bytes, os.stat_result]:
    descriptor = -1
    try:
        descriptor = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory_fd)
        status = os.fstat(descriptor)
        if not stat.S_ISREG(status.st_mode) or status.st_nlink != 1:
            raise TransactionError(f"Transaction path is not a regular single-link file: {name}")
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = -1
            content = stream.read()
    except OSError as error:
        raise TransactionError(f"Unable to read transaction file {name}: {error}") from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    if checksum is not None and _checksum(content) != checksum:
        raise TransactionError(f"Transaction checksum mismatch: {name}")
    return content, status


def _atomic_write_name(
    directory_fd: int,
    name: str,
    content: bytes,
    mode: int,
) -> None:
    temporary = f".{name}.{secrets.token_hex(8)}"
    descriptor = -1
    created = False
    try:
        descriptor = os.open(
            temporary,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
            mode,
            dir_fd=directory_fd,
        )
        created = True
        with os.fdopen(descriptor, "wb") as stream:
            descriptor = -1
            stream.write(content)
            stream.flush()
            os.fchmod(stream.fileno(), mode)
            os.fsync(stream.fileno())
        os.rename(temporary, name, src_dir_fd=directory_fd, dst_dir_fd=directory_fd)
        created = False
        _fsync_fd(directory_fd)
    except FileExistsError as error:
        raise TransactionError(f"Transaction target became occupied: {name}") from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        if created:
            try:
                os.unlink(temporary, dir_fd=directory_fd)
                _fsync_fd(directory_fd)
            except FileNotFoundError:
                pass


def _write_new_at(directory_fd: int, name: str, content: bytes, mode: int) -> None:
    descriptor = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, mode, dir_fd=directory_fd)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            descriptor = -1
            stream.write(content)
            stream.flush()
            os.fchmod(stream.fileno(), mode)
            os.fsync(stream.fileno())
        _fsync_fd(directory_fd)
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def _mkdir_at(root_fd: int, path: PurePosixPath) -> None:
    parent_fd = _open_parent(root_fd, path)
    try:
        os.mkdir(path.name, 0o755, dir_fd=parent_fd)
        _fsync_fd(parent_fd)
    finally:
        os.close(parent_fd)


def _rmdir_at(root_fd: int, path: PurePosixPath) -> None:
    parent_fd = _open_parent(root_fd, path)
    try:
        os.rmdir(path.name, dir_fd=parent_fd)
        _fsync_fd(parent_fd)
    except OSError as error:
        raise TransactionError(f"Recovery directory is not empty or removable: {path}") from error
    finally:
        os.close(parent_fd)


def _unlink_name(directory_fd: int, name: str) -> None:
    os.unlink(name, dir_fd=directory_fd)
    _fsync_fd(directory_fd)


def _capture_name(directory_fd: int, source: str, destination: str) -> None:
    if _name_exists(directory_fd, destination):
        raise TransactionError(f"Transaction capture intermediate is already occupied: {destination}")
    os.rename(source, destination, src_dir_fd=directory_fd, dst_dir_fd=directory_fd)
    _fsync_fd(directory_fd)


def _publish_name(
    directory_fd: int,
    source: str,
    destination: str,
    injector: FailureInjector | None,
    path: PurePosixPath,
) -> None:
    try:
        os.link(source, destination, src_dir_fd=directory_fd, dst_dir_fd=directory_fd, follow_symlinks=False)
    except FileExistsError as error:
        raise TransactionError(f"Transaction publication target became occupied: {path}") from error
    _fsync_fd(directory_fd)
    _inject(injector, "after_publish_link", path)
    _unlink_name(directory_fd, source)
    _inject(injector, "after_publish_unlink", path)


def _remove_recognized_name(
    directory_fd: int,
    name: str | None,
    checksum: str | None,
    mode: int | None,
) -> None:
    if name is None or not _name_exists(directory_fd, name):
        return
    if checksum is None or mode is None:
        raise TransactionError(f"Unexpected transaction intermediate exists: {name}")
    _read_named_target(directory_fd, name, checksum, mode, allow_two_links=True)
    _unlink_name(directory_fd, name)


def _name_exists(directory_fd: int, name: str) -> bool:
    try:
        os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
    except FileNotFoundError:
        return False
    return True


def _rename_at(root_fd: int, source: str, destination: str) -> None:
    os.rename(source, destination, src_dir_fd=root_fd, dst_dir_fd=root_fd)
    _fsync_fd(root_fd)


def _open_parent(root_fd: int, path: PurePosixPath) -> int:
    parent = path.parent
    if parent == PurePosixPath("."):
        return os.dup(root_fd)
    try:
        return _open_directory(root_fd, parent)
    except OSError as error:
        raise TransactionError(f"Unsafe or unavailable transaction ancestor for {path}: {error}") from error


def _open_directory(root_fd: int, path: PurePosixPath) -> int:
    descriptor = os.dup(root_fd)
    try:
        for part in path.parts:
            next_descriptor = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=descriptor)
            os.close(descriptor)
            descriptor = next_descriptor
        return descriptor
    except Exception:
        os.close(descriptor)
        raise


def _target_exists(root_fd: int, path: PurePosixPath) -> bool:
    if path.parent == PurePosixPath("."):
        parent_fd = os.dup(root_fd)
    else:
        try:
            parent_fd = _open_directory(root_fd, path.parent)
        except FileNotFoundError:
            return False
        except OSError as error:
            raise TransactionError(f"Unsafe transaction ancestor for {path}: {error}") from error
    try:
        try:
            os.stat(path.name, dir_fd=parent_fd, follow_symlinks=False)
        except FileNotFoundError:
            return False
        return True
    finally:
        os.close(parent_fd)


def _open_nearest_existing_directory(root_fd: int, path: PurePosixPath) -> int:
    candidates = (path, *path.parents) if path != PurePosixPath(".") else ()
    for candidate in candidates:
        if candidate == PurePosixPath("."):
            return os.dup(root_fd)
        try:
            return _open_directory(root_fd, candidate)
        except FileNotFoundError:
            continue
        except OSError as error:
            raise TransactionError(f"Unsafe transaction directory {candidate}: {error}") from error
    return os.dup(root_fd)


def _directory_exists(root_fd: int, path: PurePosixPath) -> bool:
    try:
        descriptor = _open_directory(root_fd, path)
    except FileNotFoundError:
        return False
    except OSError as error:
        raise TransactionError(f"Unsafe transaction directory {path}: {error}") from error
    os.close(descriptor)
    return True


def _existing_states_fd(root_fd: int) -> list[str]:
    states: list[str] = []
    for name in (STATE_DIRECTORY, PREPARING_DIRECTORY, CLEANUP_DIRECTORY):
        try:
            status = os.stat(name, dir_fd=root_fd, follow_symlinks=False)
        except FileNotFoundError:
            continue
        if not stat.S_ISDIR(status.st_mode):
            raise TransactionError(f"Transaction phase is not a regular directory: {name}")
        states.append(name)
    return states


def _record_directories(record: dict) -> list[PurePosixPath]:
    raw = record["created_directories"]
    if not isinstance(raw, list) or any(not isinstance(value, str) for value in raw):
        raise TransactionError("Transaction record directories are malformed.")
    directories = [_safe_relative(value) for value in raw]
    if directories != sorted(set(directories), key=lambda path: (len(path.parts), path.as_posix())):
        raise TransactionError("Transaction record directories are not unique and ordered.")
    return directories


def _safe_relative(value: object) -> PurePosixPath:
    if not isinstance(value, str):
        raise TransactionError("Transaction path must be text.")
    path = PurePosixPath(value)
    if path.is_absolute() or value != path.as_posix() or any(part in {"", ".", ".."} for part in path.parts):
        raise TransactionError(f"Unsafe transaction path: {value!r}")
    return path


def _fsync_fd(descriptor: int) -> None:
    try:
        os.fsync(descriptor)
    except OSError as error:
        raise TransactionError(f"Unable to durably synchronize a transaction directory: {error}") from error


def _inject(injector: FailureInjector | None, boundary: str, path: PurePosixPath) -> None:
    if injector is not None:
        injector(boundary, path)


def _valid_checksum(value: str) -> bool:
    return len(value) == 71 and value.startswith("sha256:") and all(char in "0123456789abcdef" for char in value[7:])


def _encode_evidence(content: bytes) -> str:
    return base64.b64encode(content).decode("ascii")


def _decode_evidence(value: object) -> bytes:
    if not isinstance(value, str):
        raise TransactionError("Transaction manifest evidence is malformed.")
    try:
        content = base64.b64decode(value, validate=True)
    except (ValueError, UnicodeError) as error:
        raise TransactionError("Transaction manifest evidence is malformed.") from error
    if _encode_evidence(content) != value:
        raise TransactionError("Transaction manifest evidence is not canonical.")
    return content


def _checksum(content: bytes) -> str:
    return f"sha256:{hashlib.sha256(content).hexdigest()}"
