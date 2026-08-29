# DESys Migration Recovery

Cross-snapshot corpus apply stages every target file and the target manifest on
the consumer repository filesystem. It records verified predecessor backups in
`.desys-transaction/`, mutates managed targets, and publishes
`docs/desys/corpus-manifest.yaml` last.

Transactional apply and recovery are supported only on POSIX hosts that provide
descriptor-relative filesystem operations, `O_NOFOLLOW`, advisory `flock`,
hard-link publication, and durable file and directory `fsync` (the validated
profile is Linux and macOS). Windows
continues to fail closed when transaction state exists, but transactional apply
and recovery are rejected before mutation because equivalent guarantees are not
implemented. Move the worktree to a supported filesystem and host for recovery;
do not remove state manually.

An apply failure automatically restores and verifies the predecessor. If the
process or rollback is interrupted, all DESys commands, including dry runs,
fail closed while transaction state exists.

## Recovery

1. Stop other processes that may modify the consumer repository.
2. Do not edit, move, replace, or delete `.desys-transaction/` or managed files.
3. Run `desys-project-init --root <repository> --recover` with the same trusted
   DESys package release that created the transaction.
4. If recovery reports that the predecessor was restored, retry the migration.
   If it reports that the target had already committed, no retry is needed.

Recovery rejects malformed records, symlinks, hard-linked state files, unknown
paths, untrusted manifest evidence, unauthenticated operation or managed-path
inventories, checksum mismatches, and unrecognized target bytes or permissions.
State moves through durable preparation, apply, rollback, terminal, and cleanup
phases. Recorded same-directory intermediates make publication and capture
windows recoverable. Interrupted terminal cleanup is resumed without mutating
managed targets and is re-authenticated even when staged content or backups were
already removed. Transaction state is removed only after full target or
predecessor verification. Preserve the repository for investigation if
recovery fails.
