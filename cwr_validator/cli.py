# -*- coding: utf-8 -*-
"""Command-line interface for CWR file validation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from cwr_validator.library_paths import (
    LibraryPathError,
    resolve_library_paths,
    validate_library_paths,
)
from cwr_validator.validator import ValidationResult, validate_files


def _format_result(result: ValidationResult, verbose: bool) -> str:
    name = Path(result.file).name
    if result.ok:
        if verbose:
            return (
                f"PASS  {name}  ({result.version}, "
                f"{result.groups} groups, {result.transactions} transactions)"
            )
        return f"PASS  {name}  ({result.version})"
    detail = result.error or "unknown error"
    if result.error_type:
        detail = f"{result.error_type}: {detail}"
    return f"FAIL  {name}  ({result.version})  {detail}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate CWR v2.1 (.V21) and v2.2 (.V22) files using local DataApi libraries.",
    )
    parser.add_argument(
        "files",
        nargs="+",
        type=Path,
        help="CWR files to validate",
    )
    parser.add_argument(
        "--version",
        choices=("2.1", "2.2"),
        help="Force CWR version for all files (must match .V21/.V22 extension if present)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON per file",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Only print failures",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Include group and transaction counts on success",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        paths = resolve_library_paths()
        validate_library_paths(paths)
    except LibraryPathError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 2

    results = validate_files(args.files, forced_version=args.version, paths=paths)

    if args.json:
        print(json.dumps([result.__dict__ for result in results], indent=2))
    else:
        for result in results:
            if args.quiet and result.ok:
                continue
            print(_format_result(result, args.verbose))

    if any(not result.ok for result in results):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
