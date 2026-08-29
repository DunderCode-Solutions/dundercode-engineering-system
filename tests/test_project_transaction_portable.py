from __future__ import annotations

from pathlib import Path, PurePosixPath

import pytest

from tools import project_transaction as transaction_module
from tools.init_project import PlannedOperation
from tools.project_transaction import TransactionError, guard_operation

MANIFEST = PurePosixPath("docs/desys/corpus-manifest.yaml")


def make_repository(path: Path) -> Path:
    path.mkdir()
    (path / ".git").mkdir()
    return path


def test_transaction_apply_and_recovery_refuse_unsupported_hosts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = make_repository(tmp_path / "repository")
    manifest = root / MANIFEST
    manifest.parent.mkdir(parents=True)
    manifest.write_bytes(b"before\n")
    pending = make_repository(tmp_path / "pending")
    (pending / transaction_module.PREPARING_DIRECTORY).mkdir(mode=0o700)
    operations = [
        PlannedOperation(
            "UPDATE",
            MANIFEST,
            content=b"after\n",
            expected_checksum=transaction_module._checksum(b"before\n"),
            target_checksum=transaction_module._checksum(b"after\n"),
        )
    ]

    monkeypatch.setattr(transaction_module.os, "name", "nt")
    with pytest.raises(TransactionError, match="require POSIX"):
        transaction_module.apply_transaction(
            root,
            operations,
            authenticate_record=lambda predecessor, target, entries: [],
            manifest_path=MANIFEST,
        )
    with pytest.raises(TransactionError, match="require POSIX"):
        transaction_module.recover_transaction(
            pending,
            authenticate_record=lambda predecessor, target, entries: [],
            manifest_path=MANIFEST,
        )

    assert manifest.read_bytes() == b"before\n"
    assert (pending / transaction_module.PREPARING_DIRECTORY).exists()


def test_guard_checks_lexical_and_resolved_repository_ancestry(tmp_path: Path) -> None:
    lexical_repository = make_repository(tmp_path / "lexical")
    resolved_repository = make_repository(tmp_path / "resolved")
    outside = tmp_path / "outside"
    outside.mkdir()
    (lexical_repository / transaction_module.STATE_DIRECTORY).mkdir()
    (resolved_repository / transaction_module.STATE_DIRECTORY).mkdir()

    lexical_link = lexical_repository / "link-out"
    lexical_link.symlink_to(outside, target_is_directory=True)
    with pytest.raises(TransactionError, match="Pending DESys recovery"):
        guard_operation(lexical_link / "output.yaml")

    resolved_link = outside / "link-in"
    resolved_link.symlink_to(resolved_repository, target_is_directory=True)
    with pytest.raises(TransactionError, match="Pending DESys recovery"):
        guard_operation(resolved_link / "output.yaml")
