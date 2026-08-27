#!/usr/bin/env python3
"""Validate canonical metadata across the DESys repository."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.desys_indexer.config import load_config
from tools.desys_metadata import validate_repository


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root.")
    parser.add_argument(
        "--config",
        type=Path,
        help="Restrict validation to the source and exclusion rules in an indexer configuration.",
    )
    parser.add_argument(
        "--strict-placeholders",
        action="store_true",
        help="Treat empty identifier-bearing Markdown files as errors.",
    )
    parser.add_argument(
        "--show-warnings",
        action="store_true",
        help="Print warnings in addition to validation errors.",
    )
    parser.add_argument(
        "--max-warnings",
        type=int,
        help="Fail when the warning count exceeds this governed baseline.",
    )
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    config = load_config(arguments.config) if arguments.config is not None else None
    if config is not None and arguments.root.resolve() != config.repository_root:
        print("ERROR: --root must match the configured repository_root.", file=sys.stderr)
        return 1
    report = validate_repository(
        arguments.root,
        strict_placeholders=arguments.strict_placeholders,
        sources=config.sources if config is not None else None,
        is_excluded=config.is_excluded if config is not None else None,
    )

    visible_issues = (
        report.issues
        if arguments.show_warnings
        else tuple(issue for issue in report.issues if issue.severity == "error")
    )
    for issue in visible_issues:
        print(issue)

    print(
        f"Validated {report.document_count} documents: "
        f"{len(report.errors)} error(s), {len(report.warnings)} warning(s)."
    )
    warning_limit_exceeded = (
        arguments.max_warnings is not None
        and len(report.warnings) > arguments.max_warnings
    )
    if warning_limit_exceeded:
        print(
            f"ERROR: Warning count exceeds baseline of {arguments.max_warnings}.",
            file=sys.stderr,
        )
    return 1 if report.errors or warning_limit_exceeded else 0


if __name__ == "__main__":
    raise SystemExit(main())
