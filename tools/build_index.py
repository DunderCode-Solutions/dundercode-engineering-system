#!/usr/bin/env python3
"""
DESys Documentation Index Builder

Builds the DESys knowledge indexes used by:

- DSK (DunderCode Skills)
- DSP (Documentation System Portal)

Author:
    DunderCode Engineering

Usage:

    python tools/build_index.py

    python tools/build_index.py --verbose

    python tools/build_index.py --config tools/desys_indexer.yaml

"""

import argparse
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.desys_indexer.config import ConfigurationError, load_config
from tools.desys_indexer.parser import IndexingError, parse_documents
from tools.desys_indexer.scanner import scan_markdown_documents
from tools.desys_indexer.writer import render_indexes, write_indexes
from tools.desys_metadata import validate_repository

DEFAULT_CONFIG = Path("tools/desys_indexer.yaml")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="build_index",
        description="DESys Documentation Index Builder",
    )

    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG,
        help="Indexer configuration file.",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Execute parsing without writing artifacts.",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_arguments()

    try:
        config = load_config(args.config)
    except (ConfigurationError, FileNotFoundError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    if args.verbose:
        print(f"Loading configuration: {args.config}")

    report = validate_repository(
        config.repository_root,
        sources=config.sources,
        is_excluded=config.is_excluded,
    )
    if args.verbose:
        for issue in report.warnings:
            print(issue)
    if report.errors:
        for issue in report.errors:
            print(issue, file=sys.stderr)
        print(f"Indexing aborted with {len(report.errors)} metadata error(s).", file=sys.stderr)
        return 1

    paths = scan_markdown_documents(config, verbose=args.verbose)

    try:
        documents = parse_documents(paths, repository_root=config.repository_root)
        rendered = render_indexes(documents, config.artifacts)
    except IndexingError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    if args.dry_run:
        print(
            f"Validated and rendered {len(documents)} documents "
            f"with {len(report.warnings)} warning(s) "
            f"({rendered.build_id})."
        )
        return 0

    try:
        write_indexes(
            rendered=rendered,
            output_dir=config.output_directory,
            verbose=args.verbose,
        )
    except OSError as error:
        print(f"ERROR: Unable to write index artifacts: {error}", file=sys.stderr)
        return 1

    print(
        f"DESys index successfully generated "
        f"({len(documents)} documents, {rendered.build_id})."
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
