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

from pathlib import Path
import argparse
import sys

from desys_indexer.config import load_config
from desys_indexer.scanner import scan_markdown_documents
from desys_indexer.parser import parse_documents
from desys_indexer.writer import write_indexes


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

    config = load_config(args.config)

    if args.verbose:
        print(f"Loading configuration: {args.config}")

    documents = scan_markdown_documents(
        root=config.repository_root,
        include_dirs=config.sources,
        exclude_dirs=config.exclude,
        verbose=args.verbose,
    )

    parsed_documents = parse_documents(
        documents,
        verbose=args.verbose,
    )

    if args.dry_run:
        print(f"{len(parsed_documents)} documents parsed successfully.")
        return 0

    write_indexes(
        documents=parsed_documents,
        output_dir=config.output_directory,
        artifacts=config.artifacts,
        verbose=args.verbose,
    )

    print(
        f"DESys index successfully generated "
        f"({len(parsed_documents)} documents)."
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())